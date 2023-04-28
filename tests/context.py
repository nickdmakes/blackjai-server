import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import torch

# Test if torch is using GPU
def test_torch_gpu():
    print(torch.__version__)
    print(torch.cuda.is_available())
    print(torch.cuda.get_device_properties(0))
    print(torch.version.cuda)


if __name__ == "__main__":
    test_torch_gpu()
