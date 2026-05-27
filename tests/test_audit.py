from __future__ import annotations

from renwei_zh import audit_text


def test_audit_detects_dense_ai_style() -> None:
    text = (
        "🚀 关于我们的新产品\n\n"
        "在这个不断演变的科技格局中，AI 正以巨大的速度重塑整个行业。"
        "我们的核心定位是一次撰写、多重用途，真正可贵的是这种产品视角。"
        "我想从三个维度回应你：在数据层面构建系统，在分析层面沉淀经验。"
        "这不仅仅是一次产品更新，更是行业革命。展望未来，我们将砥砺前行。"
    )
    result = audit_text(text, scenario="business")

    assert result["score"]["band"] == "rewrite"
    assert result["score"]["evidence"]["red_hits"] >= 6
    assert result["clusters"]["cluster_count"] >= 1
    assert result["model_fingerprints"][0]["model"] in {"DeepSeek", "GPT"}


def test_fact_risk_is_reported_without_claiming_authorship() -> None:
    text = "麦肯锡 2024 年报告说成功率约 12%，但这个数字需要核查。"
    result = audit_text(text, scenario="business")

    assert result["fact_risk"]["count"] >= 3
    assert "proof" not in " ".join(result["guidance"]).lower()


def test_academic_scenario_allows_academic_cliche_patterns() -> None:
    text = "本研究进行分析，综上所述，该方法具有一定必要性。"
    general = audit_text(text)
    academic = audit_text(text, scenario="academic")

    general_ids = {hit["pattern_id"] for hit in general["pattern_hits"]}
    academic_ids = {hit["pattern_id"] for hit in academic["pattern_hits"]}
    assert "academic_cliche" in general_ids
    assert "academic_cliche" not in academic_ids


def test_clean_text_gets_light_edit_guidance() -> None:
    text = "我们 6 月发了一个小功能。它解决的是客户导入数据时经常卡住的问题。还有两处边界没处理好，下周继续补。"
    result = audit_text(text, scenario="business")

    assert result["score"]["value"] >= 70
    assert result["clusters"]["cluster_count"] == 0
