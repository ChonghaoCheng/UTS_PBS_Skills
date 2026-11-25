# SSH access

Use the local client that will submit jobs. Preserve an existing working Cetus alias. For a new setup, use the account and login node approved by UTS and connect the local client to the UTS VPN when required.

```sshconfig
Host cetus
    HostName hpc-login02.hpc.uts.edu.au
    User YOUR_UTS_LOGIN
    ControlMaster auto
    ControlPath ~/.ssh/cetus-%C
    ControlPersist 30m
```

Place this in local ~/.ssh/config. Verify the host fingerprint through the university's guidance on first connection. `ssh -G cetus` shows effective settings, `ssh cetus` opens a shell, and `ssh cetus true` authenticates and exits while allowing connection reuse.

For requested key enrollment, first check that the chosen key filename is unused. Generate a passphrase-protected key and copy only its public key:

```bash
ssh-keygen -t ed25519 -f ~/.ssh/id_ed25519_cetus -C "cetus-workstation"
ssh-copy-id -o ControlPath=none -i ~/.ssh/id_ed25519_cetus.pub cetus
```

Add `IdentityFile ~/.ssh/id_ed25519_cetus` and `IdentitiesOnly yes` to the alias when using that key. Public keys go in the login account's remote `$HOME/.ssh/authorized_keys`. Keep private keys on their originating client. Use `ssh-add ~/.ssh/id_ed25519_cetus` with an active local SSH agent for unattended access to a locked key.

Verify fresh public-key authentication separately from connection reuse:

```bash
ssh -o ControlPath=none -o BatchMode=yes -o PreferredAuthentications=publickey cetus hostname
```

Then verify the environment used by the AI client can access the required commands:

```bash
ssh -o BatchMode=yes -o StrictHostKeyChecking=yes -o ConnectTimeout=10 cetus \
    'hostname; command -v qsub qstat rsync tar sha256sum'
```

- DNS failure or timeout requires checking hostname, campus/VPN connectivity and client network permissions.
- `Permission denied (publickey,...)` is authentication failure. Check username, identity and agent. An error naming `authorized_keys` may instead indicate a remote permission problem. Do not request passwords or private-key content in chat.
- A successful login via a reused socket does not prove the newly configured key works; use the fresh-key test above.
- Each direct client may use its own key. Alternatively, remote into the local submission workstation and run the AI client there. Existing jobs continue after disconnect. Keep that run's local manifest accessible to the client doing collection.

[Cetus SSH](https://cetus.hpc.uts.edu.au/getting_started/access_via_ssh/) · [Troubleshooting](https://cetus.hpc.uts.edu.au/faq/ssh/) · [OpenSSH configuration](https://man.openbsd.org/ssh_config.5)
