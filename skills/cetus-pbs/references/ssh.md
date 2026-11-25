# SSH access

Use the user's existing SSH target and configuration in the environment that will submit jobs. `cetus` below is an example alias, not a required name. The account, login host, key path and network requirements come from the user's current setup and UTS guidance. Do not copy another user's identity or paths.

For a new alias, choose a login node listed by UTS and the user's own Cetus login. The [UTS SSH guide](https://cetus.hpc.uts.edu.au/getting_started/access_via_ssh/) lists login nodes such as `hpc-login01.hpc.uts.edu.au` and `hpc-login02.hpc.uts.edu.au`; preserve a working approved target instead of replacing it with an example.

```sshconfig
Host cetus
    HostName YOUR_CETUS_LOGIN_HOST
    User YOUR_UTS_LOGIN
```

Add this to the appropriate local SSH configuration only when setup is requested. Verify the host fingerprint through UTS guidance on first connection, and use the required campus/VPN connection. `ssh -G cetus` shows effective settings, `ssh cetus` opens a shell, and `ssh cetus true` authenticates and exits. Optional connection multiplexing follows the local client's capabilities and existing settings; no socket path or persistence duration is required by this skill.

## Key setup when requested

Reuse a suitable existing identity. For a new key, choose an unused local path and a passphrase. The following key filename is an example; check both files before generation to avoid replacing an existing identity.

```bash
key_path="$HOME/.ssh/cetus_example_ed25519"
if [[ -e $key_path || -e $key_path.pub ]]; then
    printf 'Choose an unused key path before generating a key.\n' >&2
else
    ssh-keygen -t ed25519 -f "$key_path" &&
        ssh-copy-id -o ControlPath=none -i "$key_path.pub" cetus
fi
```

Add the chosen `IdentityFile` to the alias when needed, and use `IdentitiesOnly yes` when restricting the identities offered. Enroll only the public key in the remote account's `$HOME/.ssh/authorized_keys`, with appropriate account-owned directory/file permissions. Keep private keys on the originating client. Where `ssh-copy-id` is unavailable, follow the supported public-key enrollment procedure for that client/site. Use an active local SSH agent when unattended access needs a passphrase-protected key.

Verify fresh public-key authentication independently of any reused connection:

```bash
ssh -o ControlPath=none -o BatchMode=yes -o PreferredAuthentications=publickey cetus hostname
```

Then check the lightweight scheduler/transfer tools needed by the selected workflow:

```bash
ssh -o BatchMode=yes -o StrictHostKeyChecking=yes -o ConnectTimeout=10 cetus \
    'hostname; command -v qsub qstat rsync tar sha256sum'
```

These probes do not run the workload. Account enrollment or interactive authentication may require the user to act in their own terminal; do not request passwords, private keys or authentication codes in chat.

## Diagnose access

- DNS failure or timeout requires checking the target, campus/VPN connection and client network permissions.
- `Permission denied (publickey,...)` requires checking username, selected identity and agent. An error naming `authorized_keys` can indicate remote file permissions.
- A reused SSH socket can mask key-authentication failures. Use the fresh-key probe when diagnosing a newly enrolled key.
- Each submission computer may use its own identity. A user may also remote into their submission workstation and operate from there. Jobs continue independently of the client connection; retain access to their receipts and records for later collection.

[UTS SSH](https://cetus.hpc.uts.edu.au/getting_started/access_via_ssh/) · [OpenSSH configuration](https://man.openbsd.org/ssh_config.5)
