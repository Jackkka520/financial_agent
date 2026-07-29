import csv
import os
import json
from datetime import datetime

LOG_FILE = 'token_usage.log'
STATS_FILE = 'token_stats.txt'
DAILY_LIMIT_FILE = 'daily_limit.json'
MAX_TOKENS_PER_DAY = 100000  # 10 万 token 限额

def init_log():
    """Initialize log file if it doesn't exist"""
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['timestamp', 'question', 'answer', 'prompt_tokens', 'completion_tokens', 'total_tokens'])

def get_today():
    return datetime.now().strftime('%Y-%m-%d')

def get_daily_usage():
    """Get today's token usage from daily limit file"""
    if os.path.exists(DAILY_LIMIT_FILE):
        with open(DAILY_LIMIT_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            if data.get('date') == get_today():
                return data.get('tokens', 0)
    return 0

def update_daily_usage(total_tokens):
    """Update today's token usage"""
    today = get_today()
    used = get_daily_usage()
    data = {
        'date': today,
        'tokens': used + total_tokens
    }
    with open(DAILY_LIMIT_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)

def check_limit(total_tokens):
    """Check if adding tokens would exceed the daily limit"""
    used = get_daily_usage()
    if used + total_tokens > MAX_TOKENS_PER_DAY:
        return False, f"⚠️ Daily token limit reached ({MAX_TOKENS_PER_DAY:,} tokens). Please try again tomorrow."
    return True, None

def log_usage(question, answer, prompt_tokens=0, completion_tokens=0, total_tokens=0):
    """Log one API call usage and update stats"""
    # 检查限额
    can_proceed, msg = check_limit(total_tokens)
    if not can_proceed:
        print(f"❌ {msg}")
        return msg
    
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
    
    # 更新每日用量
    update_daily_usage(total_tokens)
    
    stats = get_usage_stats()
    stats['total_tokens'] += total_tokens
    stats['requests'] += 1
    _save_stats(stats)
    
    remaining = MAX_TOKENS_PER_DAY - get_daily_usage()
    print(f"📝 Logged: {question[:30]}... ({total_tokens} tokens) | Remaining today: {remaining:,} / {MAX_TOKENS_PER_DAY:,}")
    return None

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

def get_remaining_tokens():
    """Get remaining tokens for today"""
    return max(0, MAX_TOKENS_PER_DAY - get_daily_usage())

def print_usage():
    stats = get_usage_stats()
    remaining = get_remaining_tokens()
    daily_used = get_daily_usage()
    print("=" * 50)
    print(f"📊 TOKEN USAGE SUMMARY")
    print(f"   Requests: {stats['requests']}")
    print(f"   Total Tokens Used: {stats['total_tokens']:,}")
    print(f"   Today's Usage: {daily_used:,} / {MAX_TOKENS_PER_DAY:,}")
    print(f"   Remaining Today: {remaining:,}")
    print("=" * 50)