# Development Setup

If you plan on customizing your instance by making changes to Mastodon's source
code, you'll want to set up a **development environment** - basically, a sandbox
where you can play around with the code without fear of breaking anything. This
is very highly recommended over making code changes directly to your production
(live) instance, especially if you have other users who would be affected by the
potential downtime!

The official [Mastodon docs] have instructions on how to create a dev
environment using [Vagrant], if you'd like to go that route. Personally, I
prefer to cut out the intermediary, so on this page I'll be walking you through
how to manually set up a development environment **from source**.

??? question "FAQ - Why not use Vagrant?"

    Vagrant can _sometimes_ work "automagically", allowing you to get your
    development environment up and running with just a couple of commands. But
    when it doesn't, you can end up having to troubleshoot issues in a greater
    number of (relatively obscure) moving parts. Overall, I prefer to keep my
    development workflow simple by manually managing my environment - it isn't
    _that_ much more work, and avoiding Vagrant's (and VirtualBox's) finickiness
    is worth it to me.

    If you'd like to try using Vagrant, by all means go ahead! However, this
    page probably won't be of much use to you. :shiba_hide:

[mastodon docs]: https://docs.joinmastodon.org/dev/setup
[vagrant]: https://vagrantup.com

## Preparing your machine

All of the following instructions assume that you have a **Linux**[^1] machine
(and root access to it, of course). If you have a Mac, you'll probably be able
to get these instructions to work with some minor adjustments. If you're on
Windows, though, you'll probably want to look into using either [WSL 2] or a
desktop virtual machine (such as [VMware Workstation] or [Oracle VirtualBox]).

[^1]:
    A machine running Ubuntu or Debian will likely provide the most
    straightforward setup experience, but the instructions on this page should
    (roughly, and in theory) work for most Linux distros. If you notice any
    hiccups or have any tips that you think would be helpful to mention, please
    don't hesitate to open a [pull request] for [this page]! :bear_love:

[wsl 2]: https://learn.microsoft.com/en-us/windows/wsl/install
[vmware workstation]: https://www.vmware.com/products/workstation-player.html
[oracle virtualbox]: https://www.virtualbox.org
[pull request]:
  https://github.com/CutieCity/.github/blob/main/.github/contributing.md
[this page]:
  https://github.com/CutieCity/guide/blob/main/docs/self-hosting/development-setup.md

### Installing system utilities

The very first thing you'll need to do is make sure a few basic system utilities
([curl], [wget], [gnupg], [lsb-release], and [ca-certificates]) are installed,
as they'll be used throughout the rest of this guide.

```bash
sudo apt install -y curl wget gnupg lsb-release ca-certificates
```

[curl]: https://packages.debian.org/stable/curl
[wget]: https://packages.debian.org/stable/wget
[gnupg]: https://packages.debian.org/stable/gnupg
[lsb-release]: https://packages.debian.org/stable/lsb-release
[ca-certificates]: https://packages.debian.org/stable/ca-certificates

### Adding a Postgres source

You'll also need to prepare your machine to download [PostgreSQL] (the database
system used by Mastodon) by telling it _exactly_ where to find the correct
version of `postgresql`.

Run this command to set and check the `PSQL_DIST` variable, which we'll be using
shortly:

```bash
PSQL_DIST=$(lsb_release -cs) && echo $PSQL_DIST
```

??? warning "Warning - Make sure your distribution name is valid!"

    The value of `PSQL_DIST` (i.e. the output of the above command) **must match
    one** of the distributions listed by the [PostgreSQL Apt Repository]. At the
    time of writing, the valid values (a.k.a. **codenames**) are:

    <div class="grid" markdown>

    <div align="center" style="margin-bottom: -1.35em;">

    **[Debian]**
    {style="margin: 0;"}

    | Codename   | Version  |
    | :--------: | :------: |
    | `bookworm` | 12.x     |
    | `bullseye` | 11.x     |
    | `buster`   | 10.x     |
    | `sid`      | unstable |

    </div>

    <div align="center" style="margin-bottom: -1.35em;">

    **[Ubuntu]**
    {style="margin: 0;"}

    | Codename  | Version |
    | :-------: | :-----: |
    | `kinetic` | 22.10   |
    | `jammy`   | 22.04   |
    | `focal`   | 20.04   |
    | `bionic`  | 18.04   |

    </div>

    </div>

    If the output you received from the previous command **doesn't** match one
    of those eight codenames, try running:

    ```bash
    PSQL_DIST=$(cat /etc/os-release | grep UBUNTU_CODENAME | cut -d = -f 2) && echo $PSQL_DIST
    ```

    This should correct the value of `PSQL_DIST` and set you up to proceed with
    the next steps.

With `PSQL_DIST` configured properly for your system, you can run this next
command as-is to add the appropriate repository for `postgresql` to your `apt`
sources:

```bash
echo "deb [signed-by=/usr/share/keyrings/postgresql.asc] \
  http://apt.postgresql.org/pub/repos/apt $PSQL_DIST-pgdg main" |
  sudo tee -a /etc/apt/sources.list.d/postgresql.list
```

Last but not least, import the repository authentication key to allow `apt` to
validate the package:

```bash
sudo wget -O /usr/share/keyrings/postgresql.asc \
  https://www.postgresql.org/media/keys/ACCC4CF8.asc
```

[postgresql]: https://www.postgresql.org
[postgresql apt repository]: https://apt.postgresql.org/pub/repos/apt/dists/
[debian]: https://www.postgresql.org/download/linux/debian
[ubuntu]: https://www.postgresql.org/download/linux/ubuntu

## Installing the requirements

Mastodon has _a lot_ of dependencies, some of which call for more involved
management than others. We'll be tackling them in three distinct chunks:
[NodeJS], simple [system packages], and [Ruby] - in that order.

[nodejs]: #setting-up-nodejs
[system packages]: #installing-system-packages
[ruby]: #setting-up-ruby

### Setting up NodeJS

- _Under construction._

### Installing system packages

- _Under construction._

### Setting up Ruby

We'll be using [rbenv] to manage our Ruby environment because it enables
convenient switching between multiple versions (in case you have other Ruby
projects) _and_ makes it extremely easy to update whenever a new version is
released. Additionally, we'll be using rbenv's [ruby-build] plugin to power the
`rbenv install` command and thereby streamline the installation process.
:cat_wow:

[rbenv]: https://github.com/rbenv/rbenv
[ruby-build]: https://github.com/rbenv/ruby-build

First, clone the source code for both of these tools into `.rbenv` in your home
directory:

```bash
git clone https://github.com/rbenv/rbenv.git ~/.rbenv
```

```bash
git clone https://github.com/rbenv/ruby-build.git ~/.rbenv/plugins/ruby-build
```

Next, add rbenv's initialization prereqs to your `.bashrc` so they run when you
open your terminal:

```bash
echo 'export PATH="$HOME/.rbenv/bin:$PATH"' >> ~/.bashrc
```

```bash
echo 'eval "$(rbenv init -)"' >> ~/.bashrc
```

Then, reload[^2] your terminal session to execute those initialization steps:

```bash
exec bash
```

Now it's time to actually install Ruby itself. This next command may take a
while to complete:

```bash
RUBY_CONFIGURE_OPTS=--with-jemalloc rbenv install 3.2.1
```

Once that's done, set the newly installed version of Ruby as the default version
on your system:

```bash
rbenv global 3.2.1
```

[^2]:
    Technically, `exec bash` replaces your current shell process with a new one,
    and executes the contents of `.bashrc` as part of the usual startup
    procedure. Although the term "reload" is less correct than "replace" in a
    technical sense, I find it conceptually easier to understand.

## More info coming soon!
