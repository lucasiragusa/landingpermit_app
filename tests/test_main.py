from src.main import compute_batch
import pytest

@pytest.mark.parametrize("ssim_relative_path", [
    (""),
    ("")
])
def test_compute_batch():
    result = compute_batch(ssim_relative_path=ssim_relative_path)

    # assert result == 