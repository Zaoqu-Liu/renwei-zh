from __future__ import annotations

import re
import statistics
from collections import Counter
from dataclasses import dataclass
from typing import Any

from .catalog import load_catalog


@dataclass(frozen=True)
class RegexHit:
    pattern_id: str
    label: str
    severity: str
    start: int
    end: int
    match: str
    weight: float


def audit_text(text: str, *, scenario: str | None = None) -> dict[str, Any]:
    """Audit Chinese text and return machine-readable evidence."""
    if not text.strip():
        raise ValueError("input text is empty")

    catalog = load_catalog()
    hits = find_pattern_hits(text, catalog, scenario=scenario)
    metrics = {
        "length": length_metrics(text),
        "burstiness": burstiness(text),
        "connectors": connector_density(text, catalog),
        "lexical": lexical_metrics(text),
        "nominalization": nominalization_density(text, catalog),
    }
    fingerprints = model_fingerprints(text, catalog)
    clusters = cluster_density(text, hits)
    dare = friction_signals(text, catalog)
    fact_risk = fact_risk_scan(text, catalog)
    score = quality_score(hits=hits, metrics=metrics, clusters=clusters, dare=dare, fact_risk=fact_risk)

    return {
        "version": catalog["version"],
        "scenario": scenario or "auto",
        "score": score,
        "metrics": metrics,
        "pattern_hits": [hit.__dict__ for hit in hits],
        "clusters": clusters,
        "model_fingerprints": fingerprints,
        "friction_signals": dare,
        "fact_risk": fact_risk,
        "guidance": guidance(score, hits, clusters, fact_risk),
    }


def find_pattern_hits(text: str, catalog: dict[str, Any], *, scenario: str | None = None) -> list[RegexHit]:
    hits: list[RegexHit] = []
    for pattern_set in catalog["pattern_sets"]:
        scenarios = set(pattern_set.get("scenarios", ["all"]))
        if scenario and "all" not in scenarios and scenario not in scenarios:
            continue
        allow_in = set(pattern_set.get("allow_in", []))
        if scenario and scenario in allow_in:
            continue

        for pattern in pattern_set["patterns"]:
            regex = re.compile(pattern["regex"], re.MULTILINE | re.IGNORECASE)
            for match in regex.finditer(text):
                hits.append(
                    RegexHit(
                        pattern_id=pattern_set["id"],
                        label=pattern_set["label"],
                        severity=pattern_set["severity"],
                        start=match.start(),
                        end=match.end(),
                        match=match.group(0),
                        weight=float(pattern.get("weight", pattern_set.get("weight", 1.0))),
                    )
                )
    hits.sort(key=lambda item: (item.start, item.end, item.pattern_id))
    return _dedupe_overlapping_hits(hits)


def _dedupe_overlapping_hits(hits: list[RegexHit]) -> list[RegexHit]:
    deduped: list[RegexHit] = []
    occupied: set[tuple[int, int, str]] = set()
    for hit in hits:
        key = (hit.start, hit.end, hit.pattern_id)
        if key not in occupied:
            deduped.append(hit)
            occupied.add(key)
    return deduped


def length_metrics(text: str) -> dict[str, int]:
    clean = re.sub(r"\s+", "", text)
    paragraphs = [part for part in re.split(r"\n\s*\n", text.strip()) if part.strip()]
    sentences = split_sentences(text)
    return {
        "chars": len(clean),
        "paragraphs": len(paragraphs),
        "sentences": len(sentences),
    }


def split_sentences(text: str) -> list[str]:
    return [sentence.strip() for sentence in re.split(r"[。！？!?\n]+", text) if len(sentence.strip()) > 2]


def burstiness(text: str) -> dict[str, Any]:
    lengths = [len(sentence) for sentence in split_sentences(text)]
    if len(lengths) < 3:
        return {"status": "insufficient_text", "sentence_count": len(lengths)}
    mean = statistics.mean(lengths)
    std = statistics.stdev(lengths)
    cv = std / mean if mean else 0.0
    if cv < 0.30:
        band = "ai_like"
    elif cv < 0.60:
        band = "mixed"
    else:
        band = "varied"
    return {
        "cv": round(cv, 3),
        "mean": round(mean, 1),
        "std": round(std, 1),
        "min": min(lengths),
        "max": max(lengths),
        "sentence_count": len(lengths),
        "band": band,
    }


def connector_density(text: str, catalog: dict[str, Any]) -> dict[str, Any]:
    clean_chars = max(len(re.sub(r"\s+", "", text)), 1)
    by_category: dict[str, int] = {}
    total = 0
    for category, words in catalog["connectors"].items():
        count = sum(text.count(word) for word in words)
        by_category[category] = count
        total += count
    density = total * 1000 / clean_chars
    return {
        "total": total,
        "per_1000_chars": round(density, 2),
        "by_category": by_category,
        "band": "high" if density > 7 else "medium" if density > 5 else "low",
    }


def tokenize(text: str) -> list[str]:
    try:
        import jieba  # type: ignore

        return [token for token in jieba.cut(text) if token.strip() and not re.fullmatch(r"\W+", token)]
    except Exception:
        words = re.findall(r"[A-Za-z0-9_]+|[\u4e00-\u9fff]", text)
        merged: list[str] = []
        buffer: list[str] = []
        for word in words:
            if re.fullmatch(r"[\u4e00-\u9fff]", word):
                buffer.append(word)
                if len(buffer) == 2:
                    merged.append("".join(buffer))
                    buffer.clear()
            else:
                if buffer:
                    merged.append("".join(buffer))
                    buffer.clear()
                merged.append(word.lower())
        if buffer:
            merged.append("".join(buffer))
        return merged


def lexical_metrics(text: str) -> dict[str, Any]:
    tokens = tokenize(text)
    if not tokens:
        return {"status": "insufficient_text"}
    counts = Counter(tokens)
    unique = len(counts)
    total = len(tokens)
    ttr = unique / total
    hapax = sum(1 for count in counts.values() if count == 1) / unique if unique else 0
    yules_k = _yules_k(counts, total)
    return {
        "tokens": total,
        "unique": unique,
        "ttr": round(ttr, 3),
        "hapax_rate": round(hapax, 3),
        "yules_k": round(yules_k, 1),
        "top_repeated": counts.most_common(8),
    }


def _yules_k(counts: Counter[str], total: int) -> float:
    if total == 0:
        return 0.0
    frequency_of_frequencies = Counter(counts.values())
    numerator = sum(freq * count * count for count, freq in frequency_of_frequencies.items()) - total
    return 10_000 * numerator / (total * total)


def nominalization_density(text: str, catalog: dict[str, Any]) -> dict[str, Any]:
    clean_chars = max(len(re.sub(r"\s+", "", text)), 1)
    suffixes = catalog["nominalization_suffixes"]
    whitelist = set(catalog["nominalization_whitelist"])
    hits: list[str] = []
    for suffix in suffixes:
        regex = re.compile(rf"[\u4e00-\u9fff]{{1,6}}{re.escape(suffix)}")
        for match in regex.finditer(text):
            word = match.group(0)
            if word not in whitelist:
                hits.append(word)
    return {
        "total": len(hits),
        "per_1000_chars": round(len(hits) * 1000 / clean_chars, 2),
        "examples": hits[:12],
    }


def model_fingerprints(text: str, catalog: dict[str, Any]) -> list[dict[str, Any]]:
    models: list[dict[str, Any]] = []
    for model, patterns in catalog["model_fingerprints"].items():
        score = 0.0
        hits: list[dict[str, Any]] = []
        for pattern in patterns:
            matches = re.findall(pattern["regex"], text, re.MULTILINE | re.IGNORECASE)
            if matches:
                contribution = min(len(matches) * float(pattern["weight"]), float(pattern["weight"]) * 3)
                score += contribution
                hits.append({"label": pattern["label"], "count": len(matches), "contribution": round(contribution, 2)})
        if score:
            models.append({"model": model, "score": round(score, 3), "hits": hits})
    return sorted(models, key=lambda item: item["score"], reverse=True)


def cluster_density(text: str, hits: list[RegexHit], *, window: int = 300, min_types: int = 3) -> dict[str, Any]:
    clusters: list[dict[str, Any]] = []
    for index, anchor in enumerate(hits):
        window_end = anchor.start + window
        window_hits = [hit for hit in hits[index:] if hit.start <= window_end]
        types = sorted({hit.pattern_id for hit in window_hits})
        if len(types) >= min_types:
            clusters.append(
                {
                    "start": anchor.start,
                    "end": min(window_end, len(text)),
                    "unique_types": len(types),
                    "total_hits": len(window_hits),
                    "types": types,
                }
            )
    compact = _compact_clusters(clusters)
    return {
        "window": window,
        "min_types": min_types,
        "total_hits": len(hits),
        "unique_types": len({hit.pattern_id for hit in hits}),
        "cluster_count": len(compact),
        "clusters": compact[:10],
    }


def _compact_clusters(clusters: list[dict[str, Any]]) -> list[dict[str, Any]]:
    compact: list[dict[str, Any]] = []
    for cluster in clusters:
        if not compact or cluster["start"] >= compact[-1]["end"]:
            compact.append(cluster)
        elif cluster["unique_types"] > compact[-1]["unique_types"]:
            compact[-1] = cluster
    return compact


def friction_signals(text: str, catalog: dict[str, Any]) -> dict[str, Any]:
    categories: dict[str, Any] = {}
    total = 0
    for category, patterns in catalog["friction_signals"].items():
        hits: list[dict[str, Any]] = []
        for pattern in patterns:
            for match in re.finditer(pattern, text):
                hits.append({"match": match.group(0), "start": match.start(), "end": match.end()})
        total += len(hits)
        categories[category] = {"count": len(hits), "hits": hits[:8]}
    coverage = sum(1 for value in categories.values() if value["count"] > 0)
    return {
        "total": total,
        "coverage": coverage,
        "categories": categories,
        "band": "present" if total >= 2 and coverage >= 2 else "thin",
    }


def fact_risk_scan(text: str, catalog: dict[str, Any]) -> dict[str, Any]:
    risks: list[dict[str, Any]] = []
    for risk in catalog["fact_risk_patterns"]:
        regex = re.compile(risk["regex"], re.MULTILINE | re.IGNORECASE)
        for match in regex.finditer(text):
            risks.append({"label": risk["label"], "match": match.group(0), "start": match.start()})
    return {
        "count": len(risks),
        "items": risks[:20],
        "rule": "Do not add or alter these facts unless the user supplied them.",
    }


def quality_score(
    *,
    hits: list[RegexHit],
    metrics: dict[str, Any],
    clusters: dict[str, Any],
    dare: dict[str, Any],
    fact_risk: dict[str, Any],
) -> dict[str, Any]:
    red = sum(1 for hit in hits if hit.severity == "red")
    yellow = sum(1 for hit in hits if hit.severity == "yellow")
    cluster_penalty = clusters["cluster_count"] * 8
    fingerprint_penalty = min(sum(hit.weight for hit in hits), 25)
    connector_penalty = 6 if metrics["connectors"]["band"] == "high" else 3 if metrics["connectors"]["band"] == "medium" else 0
    burst_penalty = 6 if metrics["burstiness"].get("band") == "ai_like" else 2 if metrics["burstiness"].get("band") == "mixed" else 0
    friction_bonus = 4 if dare["band"] == "present" else 0
    raw = 100 - red * 4 - yellow * 1.5 - cluster_penalty - fingerprint_penalty - connector_penalty - burst_penalty + friction_bonus
    bounded = max(0, min(100, raw))
    band = "publishable" if bounded >= 86 else "needs_revision" if bounded >= 70 else "rewrite"
    return {
        "value": round(bounded, 1),
        "band": band,
        "evidence": {
            "red_hits": red,
            "yellow_hits": yellow,
            "clusters": clusters["cluster_count"],
            "fact_risk_items": fact_risk["count"],
        },
    }


def guidance(score: dict[str, Any], hits: list[RegexHit], clusters: dict[str, Any], fact_risk: dict[str, Any]) -> list[str]:
    messages: list[str] = []
    if fact_risk["count"]:
        messages.append("Fact guard: preserve numbers, citations, dates, names, and sources unless the user supplied replacements.")
    if clusters["cluster_count"]:
        messages.append("Break dense clusters first; scattered single tells are lower priority than multi-type clusters.")
    top_ids = [item for item, _ in Counter(hit.pattern_id for hit in hits).most_common(3)]
    if top_ids:
        messages.append("Priority pattern families: " + ", ".join(top_ids))
    if score["band"] == "rewrite":
        messages.append("Recommendation: rewrite structurally, not by synonym substitution.")
    elif score["band"] == "needs_revision":
        messages.append("Recommendation: revise targeted high-severity evidence and rerun the audit.")
    else:
        messages.append("Recommendation: light edit only; avoid over-humanizing.")
    return messages
