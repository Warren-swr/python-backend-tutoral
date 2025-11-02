"""
并发编程示例

本模块展示了Python中三种并发编程方式的对比
1. 多进程 (multiprocessing) - 真正的并行，每个进程独立的解释器和内存空间
2. 多线程 (threading) - 共享内存, 但受GIL限制, 适合IO密集型任务
3. 协程 (asyncio) - 单线程通过事件循环实现并发, 适合IO密集型任务
"""


import time
import threading
import multiprocessing
import asyncio
import os


# 模拟IO密集型任务（下载）
def io_task(name, task_id):
    """模拟IO密集型任务, 会释放GIL"""
    pid = os.getpid()
    thread_id = threading.current_thread().ident
    start_time = time.time()
    print(f"[{time.strftime('%H:%M:%S')}] {name} 开始 - PID:{pid}, Thread:{thread_id}")
    
    # 模拟网络IO等待（会释放GIL，让其他线程执行）
    time.sleep(2)
    
    end_time = time.time()
    elapsed = end_time - start_time
    print(f"[{time.strftime('%H:%M:%S')}] {name} 完成 - 耗时:{elapsed:.2f}s, PID:{pid}, Thread:{thread_id}")
    return task_id


# 模拟CPU密集型任务（计算）
def cpu_task(name, task_id):
    """模拟CPU密集型任务，GIL会限制线程并发"""
    pid = os.getpid()
    thread_id = threading.current_thread().ident
    start_time = time.time()
    print(f"[{time.strftime('%H:%M:%S')}] {name} 开始计算 - PID:{pid}, Thread:{thread_id}")
    
    # CPU密集型计算（GIL限制了多线程并发，基本串行执行）
    result = 0
    for i in range(10000000):
        result += i * i
    
    end_time = time.time()
    elapsed = end_time - start_time
    print(f"[{time.strftime('%H:%M:%S')}] {name} 计算完成 - 耗时:{elapsed:.2f}s, PID:{pid}, Thread:{thread_id}")
    return task_id


# ---------- 1. 多进程 ----------
def run_processes_io():
    """多进程执行IO密集型任务"""
    print("\n" + "="*60)
    print("=== 多进程 (IO密集型任务) ===")
    print("说明: 每个进程有独立的PID，真正的并行执行")
    print("="*60)
    start = time.time()
    processes = []
    for i in range(10):
        p = multiprocessing.Process(target=io_task, args=(f"进程-{i}", i))
        processes.append(p)
        p.start()
    
    for p in processes:
        p.join()
    
    total_time = time.time() - start
    print(f"\n总耗时: {total_time:.2f}s (10个任务，每个2秒)")
    print(f"效率: 几乎并行执行，总时间 ≈ 单个任务时间")


def run_processes_cpu():
    """多进程执行CPU密集型任务"""
    print("\n" + "="*60)
    print("=== 多进程 (CPU密集型任务) ===")
    print("说明: CPU密集型任务，多进程能充分利用多核CPU")
    print("="*60)
    start = time.time()
    processes = []
    for i in range(10):
        p = multiprocessing.Process(target=cpu_task, args=(f"进程-{i}", i))
        processes.append(p)
        p.start()
    
    for p in processes:
        p.join()
    
    total_time = time.time() - start
    print(f"\n总耗时: {total_time:.2f}s")
    print(f"效率: 多核并行，总时间 ≈ 单个任务时间")


# ---------- 2. 多线程 ----------
def run_threads_io():
    """多线程执行IO密集型任务"""
    print("\n" + "="*60)
    print("=== 多线程 (IO密集型任务) ===")
    print("说明: IO等待时释放GIL，线程可以并发执行")
    print("="*60)
    start = time.time()
    threads = []
    for i in range(10):
        t = threading.Thread(target=io_task, args=(f"线程-{i}", i))
        threads.append(t)
        t.start()
    
    for t in threads:
        t.join()
    
    total_time = time.time() - start
    print(f"\n总耗时: {total_time:.2f}s (10个任务，每个2秒)")
    print(f"效率: IO等待时并发，总时间 ≈ 单个任务时间")


def run_threads_cpu():
    """多线程执行CPU密集型任务"""
    print("\n" + "="*60)
    print("=== 多线程 (CPU密集型任务) ===")
    print("说明: CPU密集型任务，GIL导致实际上串行执行")
    print("="*60)
    start = time.time()
    threads = []
    for i in range(10):
        t = threading.Thread(target=cpu_task, args=(f"线程-{i}", i))
        threads.append(t)
        t.start()
    
    for t in threads:
        t.join()
    
    total_time = time.time() - start
    print(f"\n总耗时: {total_time:.2f}s")
    print(f"效率: 受GIL限制，总时间 ≈ 单个任务时间 × 任务数量")


# ---------- 3. 协程 ----------
async def async_io_task(name, task_id):
    """协程执行IO密集型任务"""
    pid = os.getpid()
    thread_id = threading.current_thread().ident
    start_time = time.time()
    print(f"[{time.strftime('%H:%M:%S')}] {name} 开始 - PID:{pid}, Thread:{thread_id}")
    
    # 异步IO等待（不会阻塞事件循环）
    await asyncio.sleep(2)
    
    end_time = time.time()
    elapsed = end_time - start_time
    print(f"[{time.strftime('%H:%M:%S')}] {name} 完成 - 耗时:{elapsed:.2f}s, PID:{pid}, Thread:{thread_id}")
    return task_id


async def run_coroutines():
    """协程执行IO密集型任务"""
    print("\n" + "="*60)
    print("=== 协程 (IO密集型任务) ===")
    print("说明: 单线程，通过事件循环实现并发，开销极小")
    print("="*60)
    start = time.time()
    tasks = [async_io_task(f"协程-{i}", i) for i in range(10)]
    await asyncio.gather(*tasks)
    
    total_time = time.time() - start
    print(f"\n总耗时: {total_time:.2f}s (10个任务，每个2秒)")
    print(f"效率: 事件循环并发，总时间 ≈ 单个任务时间，开销最小")


async def async_cpu_task_pure(name, task_id):
    """协程执行纯CPU密集型任务（会阻塞事件循环）"""
    pid = os.getpid()
    thread_id = threading.current_thread().ident
    start_time = time.time()
    print(f"[{time.strftime('%H:%M:%S')}] {name} 开始计算 - PID:{pid}, Thread:{thread_id}")
    
    # 纯CPU计算（会阻塞事件循环，协程无法并发）
    result = 0
    for i in range(10000000):
        result += i * i
    
    end_time = time.time()
    elapsed = end_time - start_time
    print(f"[{time.strftime('%H:%M:%S')}] {name} 计算完成 - 耗时:{elapsed:.2f}s, PID:{pid}, Thread:{thread_id}")
    return task_id


async def async_cpu_task_with_yield(name, task_id):
    """协程执行CPU密集型任务（通过yield让出控制权）"""
    pid = os.getpid()
    thread_id = threading.current_thread().ident
    start_time = time.time()
    print(f"[{time.strftime('%H:%M:%S')}] {name} 开始计算 - PID:{pid}, Thread:{thread_id}")
    
    # CPU计算，但每100万次迭代让出控制权（效率会降低）
    result = 0
    for i in range(10000000):
        result += i * i
        if i % 1000000 == 0:  # 每100万次让出控制权
            await asyncio.sleep(0)  # 让出控制权给其他协程
    
    end_time = time.time()
    elapsed = end_time - start_time
    print(f"[{time.strftime('%H:%M:%S')}] {name} 计算完成 - 耗时:{elapsed:.2f}s, PID:{pid}, Thread:{thread_id}")
    return task_id


async def async_cpu_task_with_executor(name, task_id):
    """协程通过线程池执行CPU密集型任务"""
    pid = os.getpid()
    thread_id = threading.current_thread().ident
    start_time = time.time()
    print(f"[{time.strftime('%H:%M:%S')}] {name} 开始计算 - PID:{pid}, Thread:{thread_id}")
    
    # 在线程池中执行CPU密集型任务（可以并发，但受GIL限制）
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(None, cpu_task, name, task_id)
    
    end_time = time.time()
    elapsed = end_time - start_time
    print(f"[{time.strftime('%H:%M:%S')}] {name} 计算完成 - 总耗时:{elapsed:.2f}s, PID:{pid}, Thread:{thread_id}")
    return result


async def run_coroutines_cpu_pure():
    """协程执行纯CPU密集型任务（会阻塞）"""
    print("\n" + "="*60)
    print("=== 协程 (纯CPU密集型任务 - 阻塞方式) ===")
    print("说明: 纯CPU计算会阻塞事件循环，协程无法并发")
    print("="*60)
    start = time.time()
    tasks = [async_cpu_task_pure(f"协程-{i}", i) for i in range(3)]
    await asyncio.gather(*tasks)
    
    total_time = time.time() - start
    print(f"\n总耗时: {total_time:.2f}s")
    print(f"效率: 事件循环被阻塞，完全串行执行，总时间 ≈ 单个任务时间 × 任务数量")


async def run_coroutines_cpu_with_yield():
    """协程执行CPU密集型任务（通过yield）"""
    print("\n" + "="*60)
    print("=== 协程 (CPU密集型任务 - 带yield) ===")
    print("说明: 通过yield让出控制权可以并发，但效率降低")
    print("="*60)
    start = time.time()
    tasks = [async_cpu_task_with_yield(f"协程-{i}", i) for i in range(10)]
    await asyncio.gather(*tasks)
    
    total_time = time.time() - start
    print(f"\n总耗时: {total_time:.2f}s")
    print(f"效率: 可以并发，但yield开销导致效率降低，不推荐")


async def run_coroutines_cpu_with_executor():
    """协程通过线程池执行CPU密集型任务"""
    print("\n" + "="*60)
    print("=== 协程 (CPU密集型任务 - 使用线程池) ===")
    print("说明: 通过run_in_executor在线程池执行，可并发但受GIL限制")
    print("="*60)
    start = time.time()
    tasks = [async_cpu_task_with_executor(f"协程-{i}", i) for i in range(10)]
    await asyncio.gather(*tasks)
    
    total_time = time.time() - start
    print(f"\n总耗时: {total_time:.2f}s")
    print(f"效率: 线程池并发，但受GIL限制，总时间 ≈ 单个任务时间 × 任务数量")


if __name__ == "__main__":
    print("\n" + "="*60)
    print("Python并发编程对比演示")
    print("="*60)
    
    # IO密集型任务对比
    run_processes_io()
    run_threads_io()
    asyncio.run(run_coroutines())
    
    # CPU密集型任务对比（展示GIL的影响）
    run_processes_cpu()
    run_threads_cpu()
    
    # 协程CPU密集型任务演示（展示协程的局限性）
    asyncio.run(run_coroutines_cpu_pure())
    asyncio.run(run_coroutines_cpu_with_yield())
    asyncio.run(run_coroutines_cpu_with_executor())
    
    print("\n" + "="*60)
    print("总结:")
    print("1. 多进程: 适合CPU密集型，真正并行，但开销大")
    print("2. 多线程: 适合IO密集型，共享内存，但受GIL限制")
    print("3. 协程: 适合IO密集型，单线程高效并发，开销最小")
    print("    - 纯CPU任务: 会阻塞事件循环，无法并发")
    print("    - 使用yield: 可以并发但效率降低，不推荐")
    print("    - 使用executor: 可在线程池中执行，但受GIL限制")
    print("="*60)
