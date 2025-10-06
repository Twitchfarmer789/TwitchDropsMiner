# accounts.py
# Initial stub for multi-account support
from dataclasses import dataclass, field
from typing import List, Optional
import json
import os

ACCOUNTS_FILE = 'accounts.json'

@dataclass
class Account:
    username: str
    display_name: Optional[str] = None
    cookies_file: Optional[str] = None  # path to cookies jar per account

@dataclass
class AccountsConfig:
    accounts: List[Account] = field(default_factory=list)
    active: Optional[str] = None  # username of active account

    def get_active(self) -> Optional[Account]:
        for a in self.accounts:
            if a.username == self.active:
                return a
        return None


def load_accounts() -> AccountsConfig:
    if not os.path.exists(ACCOUNTS_FILE):
        return AccountsConfig()
    try:
        with open(ACCOUNTS_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
        accounts = [Account(**a) for a in data.get('accounts', [])]
        return AccountsConfig(accounts=accounts, active=data.get('active'))
    except Exception:
        # Fallback to empty config if corrupted
        return AccountsConfig()


def save_accounts(cfg: AccountsConfig) -> None:
    data = {
        'accounts': [a.__dict__ for a in cfg.accounts],
        'active': cfg.active,
    }
    with open(ACCOUNTS_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)


def set_active(username: str) -> None:
    cfg = load_accounts()
    if username not in [a.username for a in cfg.accounts]:
        raise ValueError(f'Unknown account: {username}')
    cfg.active = username
    save_accounts(cfg)


def add_or_update_account(username: str, display_name: Optional[str] = None, cookies_file: Optional[str] = None) -> None:
    cfg = load_accounts()
    for a in cfg.accounts:
        if a.username == username:
            a.display_name = display_name or a.display_name
            a.cookies_file = cookies_file or a.cookies_file
            break
    else:
        cfg.accounts.append(Account(username=username, display_name=display_name, cookies_file=cookies_file))
        if not cfg.active:
            cfg.active = username
    save_accounts(cfg)


def remove_account(username: str) -> None:
    cfg = load_accounts()
    cfg.accounts = [a for a in cfg.accounts if a.username != username]
    if cfg.active == username:
        cfg.active = cfg.accounts[0].username if cfg.accounts else None
    save_accounts(cfg)
