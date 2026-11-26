# SSH access

Use the user's existing SSH target and configuration in the environment that will submit jobs. `cetus` below is an example alias, not a required name. The account, login host, key path and network requirements come from the user's current setup and UTS guidance. Do not copy another user's identity or paths.

## Connection prerequisites

- **Campus network or UTS VPN**: Connecting from outside the UTS campus network requires an active **UTS VPN** session. Without VPN, DNS resolution or TCP connections to Cetus login nodes typically time out. Check VPN connectivity before modifying SSH settings.
- **Login nodes and username**: The [UTS SSH guide](https://cetus.hpc.uts.edu.au/getting_started/access_via_ssh/) lists login nodes such as `hpc-login01.hpc.uts.edu.au` and `hpc-login02.hpc.uts.edu.au`; preserve a working approved target instead of replacing it with an example. UTS Cetus usernames typically use `u` followed by the UTS staff or student ID (for example `u123456`); confirm the user's actual login when no existing SSH config is present.

```sshconfig
Host cetus
    HostName YOUR_CETUS_LOGIN_HOST
    User YOUR_UTS_LOGIN
```

Add this to the appropriate local SSH configuration (`~/.ssh/config`, or `$HOME\.ssh\config` on native Windows) only when setup is requested. Verify the host fingerprint through UTS guidance on first connection. `ssh -G cetus` shows effective settings, `ssh cetus` opens a shell, and `ssh -o BatchMode=yes -o ConnectTimeout=10 cetus true` tests non-interactive authentication and exits. Optional connection multiplexing follows the local client's capabilities and existing settings; no socket path or persistence duration is required by this skill.

## Key setup when requested

First test whether non-interactive access already works. When a new key is needed, split setup into local preparation by the assistant and one-time interactive enrollment by the user in their own terminal. **Never ask for passwords, private keys or MFA codes in chat.**

1. **Generate an unused local key and configure the host entry** (the filename below is an example; check both files first to avoid overwriting an existing identity):

```bash
key_path="$HOME/.ssh/cetus_example_ed25519"
if [[ -e $key_path || -e $key_path.pub ]]; then
    printf 'Choose an unused key path before generating a key.\n' >&2
else
    ssh-keygen -t ed25519 -f "$key_path"
fi
```

Add `IdentityFile ~/.ssh/cetus_example_ed25519` to the `Host cetus` block when needed, and use `IdentitiesOnly yes` when restricting the identities offered. Keep private keys on the originating client. Use an active local SSH agent when unattended access needs a passphrase-protected key.

2. **Hand the one-time enrollment command to the user**: Because initial enrollment requires interactive password/MFA entry (and first-connect host fingerprint confirmation), ask the user to run the enrollment command once in their own terminal:

Linux, macOS, WSL or Git Bash (when `ssh-copy-id` is available):

```bash
ssh-copy-id -o ControlPath=none -i "$HOME/.ssh/cetus_example_ed25519.pub" cetus
```

Native Windows PowerShell (where `ssh-copy-id` is unavailable):

```powershell
Get-Content "$HOME\.ssh\cetus_example_ed25519.pub" | ssh -o ControlPath=none cetus "umask 077; mkdir -p ~/.ssh && cat >> ~/.ssh/authorized_keys"
```

Enroll only the public key in the remote account's `$HOME/.ssh/authorized_keys` with account-owned `700`/`600` permissions (`umask 077`).

3. **Verify fresh public-key authentication and remote tools**: Once the user confirms enrollment, verify public-key login independently of any reused multiplexing socket:

```bash
ssh -o ControlPath=none -o BatchMode=yes -o PreferredAuthentications=publickey cetus hostname
```

Then check the lightweight scheduler and archive tools on the login node:

```bash
ssh -o BatchMode=yes -o StrictHostKeyChecking=yes -o ConnectTimeout=10 cetus \
    'hostname; command -v qsub qstat rsync tar sha256sum'
```

These probes do not run the workload. Remote `rsync` is used on Cetus nodes by `job.pbs`; if the **local** submission machine lacks `rsync` (common on native Windows without WSL), verify local `ssh` and `tar` and use the `tar`-over-`ssh` transfer commands in `references/pbs.md`.

## Diagnose access

- **DNS failure or connection timeout**: Verify the hostname, active campus/UTS VPN connection and local client/sandbox network permissions first.
- **`Permission denied (publickey,...)`**: Check the `u`-prefixed UTS username, `IdentityFile`, local `ssh-agent` state, and whether the user has completed the interactive public-key enrollment step. Errors mentioning `authorized_keys` or ignored keys often indicate overly permissive remote `~/.ssh` or `~/.ssh/authorized_keys` permissions.
- **Masked key failures**: A reused SSH `ControlPath` socket can hide broken key setup until the master session closes. Always run the `ControlPath=none` probe when verifying a newly enrolled key.
- **Multiple environments**: Native Windows (`$HOME\.ssh\config`) and WSL (`~/.ssh/config`) maintain separate SSH configurations and keys. Verify access in the exact environment where the agent executes commands. Jobs continue on Cetus independently of the client connection; retain receipts and local run records for later collection.

[UTS SSH](https://cetus.hpc.uts.edu.au/getting_started/access_via_ssh/) · [OpenSSH configuration](https://man.openbsd.org/ssh_config.5)
