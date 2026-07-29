import csv
import os
from datetime import datetime

LOG_FILE = 'token_usage.log'
STATS_FILE = 'token_stats.txt'

def init_log():
    """Initialize log file if it doesn't exist"""
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['timestamp', 'question', 'answer', 'prompt_tokens', 'completion_tokens', 'total_tokens'])

def log_usage(question, answer, prompt_tokens=0, completion_tokens=0, total_tokens=0):
    """Log one API call usage and update stats"""
    init_log()
    
    with open(LOG_FILE, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([
            datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            question,
            answer[:200] + '...' if len(answer) > 200 else answer,
            prompt_tokens,
            completion_tokens,
            total_tokens
        ])
    
    stats = get_usage_stats()
    stats['total_tokens'] += total_tokens
    stats['requests'] += 1
    _save_stats(stats)
    
    print(f"📝 Logged: {question[:30]}... ({total_tokens} tokens) | Total: {stats['total_tokens']} tokens")

def _save_stats(stats):
    with open(STATS_FILE, 'w', encoding='utf-8') as f:
        f.write(f"requests={stats['requests']}\n")
        f.write(f"total_tokens={stats['total_tokens']}\n")
        f.write(f"last_updated={datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

def get_usage_stats():
    stats = {'requests': 0, 'total_tokens': 0}
    if os.path.exists(STATS_FILE):
        with open(STATS_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                if line.startswith('requests='):
                    stats['requests'] = int(line.strip().split('=')[1])
                elif line.startswith('total_tokens='):
                    stats['total_tokens'] = int(line.strip().split('=')[1])
    return stats

def get_remaining_tokens(free_limit=2000000):
    stats = get_usage_stats()
    return max(0, free_limit - stats['total_tokens'])

def print_usage():
    stats = get_usage_stats()
    remaining = get_remaining_tokens()
    print("=" * 50)
    print(f"📊 TOKEN USAGE SUMMARY")
    print(f"   Requests: {stats['requests']}")
    print(f"   Total Tokens Used: {stats['total_tokens']:,}")
    print(f"   Remaining Tokens: {remaining:,} / 2,000,000")
    print("=" * 50)