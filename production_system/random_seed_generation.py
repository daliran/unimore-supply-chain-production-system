import random
import os

def generate_seed_pool(master_seed: int, number_of_seeds=2) -> list[int]:
    random.seed(master_seed)
    return [random.randint(0, 1_000_000) for _ in range(number_of_seeds)]

def set_global_seed(seed: int) -> None:

    # Python built-in random
    random.seed(seed)
    
    # NumPy
    '''
    np.random.seed(seed)
    '''
    
    # PyTorch
    '''try:
        import torch
        torch.manual_seed(seed)
        if torch.cuda.is_available():
            torch.cuda.manual_seed_all(seed)
    except ImportError:
        pass
    '''

    # Set Python hash seed for reproducibility
    os.environ['PYTHONHASHSEED'] = str(seed)
    

if __name__ == "__main__":
    seed_pool = generate_seed_pool(42, 100)
    print(seed_pool)