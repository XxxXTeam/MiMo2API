"""MiMo 模型定义与解析。"""

from dataclasses import dataclass
from typing import Dict, List, Tuple


MODEL_CREATED_AT = 1774937422
MODEL_OWNER = "xiaomi"
DEFAULT_MODEL = "mimo-v2.5-pro"


@dataclass(frozen=True)
class ModelInfo:
    """模型元数据。"""

    model_id: str
    name: str
    remark: str


MODEL_INFOS: Tuple[ModelInfo, ...] = (
    ModelInfo("mimo-v2.5-pro", "MiMo-V2.5-Pro", "默认旗舰模型 (开源性能旗舰)"),
    ModelInfo("mimo-v2.5", "MiMo-V2.5", "全模态理解大模型 (支持翻译/视觉问答)"),
    ModelInfo("mimo-v2-flash-studio", "MiMo-V2-Flash", "极速推理轻量级模型"),
    ModelInfo("mimo-v2-flash", "MiMo-V2-Flash", "极速推理轻量级大模型 (旧版ID)"),
    ModelInfo("mimo-v2-pro", "MiMo-V2-Pro", "深度思考模型 (旧版ID)"),
    ModelInfo("mimo-v2-omni", "MiMo-V2-Omni", "支持多模态生文 (旧版ID)"),
)

MODEL_ID_SET = {model.model_id for model in MODEL_INFOS}
MODEL_INFO_MAP: Dict[str, ModelInfo] = {
    model.model_id: model for model in MODEL_INFOS
}


def resolve_model_options(requested_model: str, reasoning_effort: str = "") -> dict:
    """解析请求模型与附加选项。"""

    model = requested_model or DEFAULT_MODEL
    thinking = bool(reasoning_effort)
    search_enabled = False

    suffixes = ("-thinking-search", "-search-thinking", "-thinking", "-search")
    changed = True
    while changed:
        changed = False
        for suffix in suffixes:
            if not model.endswith(suffix):
                continue
            model = model[: -len(suffix)]
            if "thinking" in suffix:
                thinking = True
            if "search" in suffix:
                search_enabled = True
            changed = True
            break

    if model not in MODEL_ID_SET:
        model = DEFAULT_MODEL

    return {
        "requested_model": requested_model or DEFAULT_MODEL,
        "upstream_model": model,
        "thinking": thinking,
        "search_enabled": search_enabled,
    }


def build_model_list(include_variants: bool = True) -> List[dict]:
    """构造 OpenAI 兼容模型列表。"""

    models: List[dict] = []
    variant_suffixes = (
        "",
        "-thinking",
        "-search",
        "-thinking-search",
        "-search-thinking",
    )

    for model in MODEL_INFOS:
        for suffix in (variant_suffixes if include_variants else ("", )):
            models.append({
                "created": MODEL_CREATED_AT,
                "id": f"{model.model_id}{suffix}",
                "object": "model",
                "owned_by": MODEL_OWNER,
            })

    return models
