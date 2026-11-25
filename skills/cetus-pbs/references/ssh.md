# SSH access and troubleshooting

Use the workstation or other client that will actually run the PBS commands. From off campus, connect that client to the UTS VPN. Use the user's existing alias and an official Cetus login hostname. Verify the host key using the UTS guidance before accepting a new host. `ssh -G cetus` shows effective local configuration.

```sshconfig
Host cetus hpc-login02.hpc.uts.edu.au
    HostName hpc-login02.hpc.uts.edu.au
    User YOUR_UTS_LOGIN
    ControlMaster auto
    ControlPath ~/.ssh/cetus-%C
    ControlPersist 30m
```

Keep an existing working hostname and login instead of replacing them with the example. `ssh cetus` opens a shell. `ssh cetus true` authenticates and exits after a no-op, which can start a reusable connection. Verify unattended access from the same environment that will submit:

```bash
ssh -o BatchMode=yes -o StrictHostKeyChecking=yes -o ConnectTimeout=8 cetus \
    'hostname; command -v qsub qstat rsync'
```

## Enroll a key only when requested

Use an unused filename for a passphrase-protected key. Keep the private key on the client. Upload only the `.pub` file.

```bash
ssh-keygen -t ed25519 -f ~/.ssh/id_ed25519_cetus -C "cetus-$(hostname -s)"
ssh-copy-id -o ControlPath=none -i ~/.ssh/id_ed25519_cetus.pub cetus
```

The public key belongs in the remote login account's `$HOME/.ssh/authorized_keys`. The experiment data directory is separate. Set `IdentityFile ~/.ssh/id_ed25519_cetus` and `IdentitiesOnly yes` for the alias when using the dedicated key. Unlock it with `ssh-add ~/.ssh/id_ed25519_cetus` in an active SSH agent. Test fresh public-key authentication without a reused connection:

```bash
ssh -o ControlPath=none -o BatchMode=yes -o PreferredAuthentications=publickey cetus hostname
```

## Common branches

- DNS failure or connection timeout: verify the effective hostname, campus/VPN connectivity, and whether the execution environment permits network access.
- `Permission denied (publickey,...)`: authentication failed. Check alias username, agent and configured identity, and whether a one-time interactive UTS login is possible. If the error names `authorized_keys` or a remote directory, inspect the login home and permissions instead. Never ask for a password or private key in chat.
- Existing authenticated control socket: reuse it with the same target. If `CETUS_CONTROL_PATH` points to an obsolete manual socket, unset it to use `~/.ssh/config`.
- Multiple computers: either remote into the main local submission workstation, or configure each direct client with its own key and the same alias. Run the AI CLI on that workstation/client; Cetus access is through SSH commands. PBS jobs continue independently of the client connection. Local run manifests must be accessible to the client that uses repo-level `status` and `collect`.

[Cetus SSH access](https://cetus.hpc.uts.edu.au/getting_started/access_via_ssh/) · [Cetus SSH troubleshooting](https://cetus.hpc.uts.edu.au/faq/ssh/) · [OpenSSH client configuration](https://man.openbsd.org/ssh_config.5).
