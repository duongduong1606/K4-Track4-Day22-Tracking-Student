"""Kiểm thử cấu hình chấm mà không cần dữ liệu lab hay mạng."""

import json
from pathlib import Path

import pytest

from evaluate_practice import _load_eval_config


def test_load_eval_config_prefers_json(tmp_path: Path) -> None:
    config_path = tmp_path / "video_1" / "eval_config.json"
    config_path.parent.mkdir(parents=True)
    expected = {"benchmark": "BENCH", "split": "val"}
    config_path.write_text(json.dumps(expected), encoding="utf-8")

    assert _load_eval_config(tmp_path) == expected


def test_load_eval_config_falls_back_to_seqinfo(tmp_path: Path) -> None:
    seqinfo_path = tmp_path / "video_1" / "seqinfo.ini"
    seqinfo_path.parent.mkdir(parents=True)
    seqinfo_path.write_text("[Sequence]\nname=BENCH-02-DETECTOR\n", encoding="utf-8")

    assert _load_eval_config(tmp_path) == {"benchmark": "BENCH", "split": "train"}


def test_load_eval_config_rejects_unknown_sequence_name(tmp_path: Path) -> None:
    seqinfo_path = tmp_path / "video_1" / "seqinfo.ini"
    seqinfo_path.parent.mkdir(parents=True)
    seqinfo_path.write_text("[Sequence]\nname=khong-hop-le\n", encoding="utf-8")

    with pytest.raises(ValueError, match="Không suy ra được benchmark"):
        _load_eval_config(tmp_path)


def test_load_eval_config_requires_metadata(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError, match="eval_config.json"):
        _load_eval_config(tmp_path)
