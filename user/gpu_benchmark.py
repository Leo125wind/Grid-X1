import time
import sys
import subprocess
import platform
import os

def install_torch():
    print("[-] PyTorch not found. Installing GPU support (this may take 2-3 mins)...")
    # Installs the light version (CPU+CUDA) to save bandwidth
    cmd = [sys.executable, "-m", "pip", "install", "torch", "--index-url", "https://download.pytorch.org/whl/cu118"]
    subprocess.check_call(cmd)
    print("[+] Installation Complete. Restarting script...")
    os.execv(sys.executable, ['python3'] + sys.argv)

try:
    import torch
except ImportError:
    install_torch()

def get_gpu_name():
    try:
        if torch.cuda.is_available():
            return torch.cuda.get_device_name(0)
    except:
        pass
    return "None"

def benchmark():
    print("="*50)
    print(f"🚀 GRID-X GPU BENCHMARK")
    print("="*50)

    # 1. Hardware Check
    if not torch.cuda.is_available():
        print("❌ CRITICAL: No NVIDIA GPU detected!")
        print("   (Did the host pass the GPU correctly?)")
        print("   Running in CPU-Only mode (Slow).")
        device = torch.device("cpu")
    else:
        gpu_name = get_gpu_name()
        vram = torch.cuda.get_device_properties(0).total_memory / 1e9
        print(f"✅ GPU DETECTED: {gpu_name}")
        print(f"   VRAM: {vram:.2f} GB")
        print(f"   CUDA Version: {torch.version.cuda}")
        device = torch.device("cuda")

    print("\n[1] Starting Stress Test...")
    
    # 2. Define Matrix Size (N x N)
    # 8000x8000 matrix = ~64 million calculations
    N = 8000 
    
    print(f"    Creating Matrices ({N}x{N})...", end="", flush=True)
    
    # Create random data on GPU directly
    start_setup = time.time()
    x = torch.randn(N, N, device=device)
    y = torch.randn(N, N, device=device)
    
    # Wait for GPU to finish allocation
    if device.type == 'cuda': torch.cuda.synchronize()
    print(f" Done ({time.time() - start_setup:.2f}s)")

    # 3. The Math (Matrix Multiplication)
    print(f"    Running Multiplication...", end="", flush=True)
    
    start_math = time.time()
    result = torch.matmul(x, y)
    
    if device.type == 'cuda': torch.cuda.synchronize()
    end_math = time.time()
    
    duration = end_math - start_math
    ops = (2 * N**3) / duration / 1e12 # TFLOPS calculation roughly
    
    print(f" Done!")
    print("-" * 50)
    print(f"🏁 RESULTS:")
    print(f"   Time Taken: {duration:.4f} seconds")
    print(f"   Performance: ~{ops:.2f} TFLOPS (Theoretical)")
    
    if duration < 1.0:
        print("\n🚀 RATING: INSANE SPEED (Enterprise Grade)")
    elif duration < 5.0:
        print("\n🏎️  RATING: HIGH PERFORMANCE (Gaming GPU)")
    else:
        print("\n🐢 RATING: STANDARD (or CPU Mode)")
        
    print("="*50)

if __name__ == "__main__":
    benchmark()