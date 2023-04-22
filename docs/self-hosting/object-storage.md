# Object Storage

This page will walk you through how to get your Mastodon instance set up with an
external **object storage provider** - basically, a media file storage service
in the cloud. This is _technically_ an optional step, but **very highly
recommended**, as it will save you from trouble down the road.

Affordable VPS setups typically aren't very generous with their storage space,
and it isn't efficient to make regular backups of all those media files, so do
your future self a favor and set this up!

In the words of the official [Mastodon documentation]:

> Mastodon can save files that you and your users upload on the hard disk drive
> of the VPS it runs on, however, the hard disk drive is usually not infinite
> and difficult to upgrade later. An object storage provider gives you
> practically infinite metered file storage.

> **How to get:** Amazon S3, Exoscale, Wasabi, Google Cloud, anything that
> exposes either an S3-compatible or OpenStack Swift-compatible API. Comes with
> a monthly cost based on the amount of files stored as well as how often they
> are accessed.

Those providers are all valid choices, as are self-hosted options like [Garage]
& [MinIO]. Personally, I decided to go with [Storj], so this page will be
focused on how to get set up with their service. :blobfox_box:

[mastodon documentation]: https://docs.joinmastodon.org/user/run-your-own/
[garage]: https://garagehq.deuxfleurs.fr/
[minio]: https://min.io/
[storj]: https://www.storj.io/

## Getting started with Storj

The first thing you'll need to do is [create a Storj account]. Make sure the
correct **satellite** (i.e. your geographic region) is selected - currently, the
available options are **US1**, **EU1**, and **AP1**. You don't need to provide
your payment information until you hit the limits of their [free plan]:

- 25 GB of static object storage
- 25 GB of download bandwidth per month
- 10,000 [segments] in total

### Creating a bucket

Once you've activated your account and successfully signed in, navigate to your
**Buckets** page and create the bucket that will hold all of your instance's
media files. Bucket names have to be unique, so pick something cute and
relevant! (The bucket for [cutie.city] is named `cutiecity`, in case that's a
helpful example. :zerotwo_derp:)

### Obtaining an API key

Next, navigate to your **Access** page. You should see a menu that looks like
this:

![](/images/object-storage_manage-access.png "A screenshot of the Access
Management page on Storj. Three sections are displayed: "Access Grant", "S3
Credentials", and "API Key". The blue action button in the API Key section reads
"Create Keys for CLI" and is circled in pink."){.preview data-gallery="access"}

<!-- prettier-ignore -->
Click the "Create Keys for CLI" button in the **API Key** section (it's circled
in the above screenshot). Put in whatever name you want, check the box to select
^^all^^ the permissions, and then click the "Create Keys" button. You'll be
shown the resulting **Satellite Address** and **API Key**, but don't worry about
using them right now - just click "Download .txt" and put the file somewhere
safe.
{style="margin-bottom: 10px;"}

<div class="grid two-columns" style="margin: 0;" markdown>
<figure style="width: 100%;" markdown>

![](/images/object-storage_create-key.png "A screenshot of the "Create Access"
modal dialog. The type is set to "API Access", the name is set to "Kiki" (but
this is unimportant), and the checkbox for "All" permissions is checked and
circled in pink. The remaining options are untouched, and display their default
values."){.preview data-gallery="api-key" style="object-position: 0 42%;"}

</figure>
<figure style="width: 100%;" markdown>

![](/images/object-storage_download-key.png "A screenshot of the success dialog
displayed after clicking the "Create Keys" button in the previous image. At the
bottom, there is a large blue button labeled "Download .txt". It's circled in
pink. The "Satellite Address" and "API Key" are visible. (Don't worry, I've
revoked this particular key!)"){.preview data-gallery="api-key"}

</figure>
</div>

<p style="margin-top: 0; text-align: center;" markdown>
<small style="font-style: italic;">

**Tip:** Click on any of these images to expand them, or hover over them to view
an image description.

</small>
</p>

[create a storj account]: https://storj.io/signup
[free plan]:
  https://docs.storj.io/dcs/billing-payment-and-accounts-1/pricing/free-tier
[segments]: https://docs.storj.io/dcs/concepts/definitions
[cutie.city]: https://cutie.city

## Navigating the Storj CLI

We're done with the Storj web interface for now! The next steps will make use of
their [Uplink] CLI tool, which provides the easiest way to generate all of the
configuration variables that you need to connect your Mastodon instance to your
Storj bucket.

[uplink]: https://docs.storj.io/dcs/downloads/download-uplink-cli

### Installing Uplink

=== "Linux"

    Execute the following commands in your terminal.

    ```bash
    ZIP=uplink_linux_$(dpkg --print-architecture).zip
    ```
    ```bash
    curl -L "https://github.com/storj/storj/releases/latest/download/$ZIP" -o $ZIP
    ```
    ```bash
    unzip -o $ZIP
    ```
    ```bash
    sudo install uplink '/usr/local/bin/uplink'
    ```

=== "macOS"

    Execute the following commands in your terminal.

    ```bash
    curl -L 'https://github.com/storj/storj/releases/latest/download/uplink_darwin_amd64.zip' -o uplink_darwin_amd64.zip
    ```
    ```bash
    unzip -o uplink_darwin_amd64.zip
    ```
    ```bash
    sudo install uplink '/usr/local/bin/uplink'
    ```

=== "Windows"

    1. Download the [Windows binary zip file] for Uplink.

    2. Right-click the downloaded file and select "Extract All". You can put the
       contents in whatever folder you want, but your home folder (i.e.
       `C:\Users\YOUR_NAME`) is recommended.

    3. Don't bother trying to open the `uplink.exe` file - it's only usable via
       the command line.

    4. Open your terminal of choice (e.g. PowerShell) and `cd` into the folder
       where you put the `uplink.exe` file. (If you put it in your home folder,
       you don't need to `cd`.)

[windows binary zip file]:
  https://github.com/storj/storj/releases/latest/download/uplink_windows_amd64.zip

### Running the setup wizard

=== "Linux"

    ```console
    uplink setup
    ```

=== "macOS"

    ```console
    uplink setup
    ```

=== "Windows"

    ```console
    .\uplink.exe setup
    ```

When asked to enter a name, you can leave it blank (i.e. just hit ++enter++).
You'll then be asked for information from the `.txt` file you downloaded
earlier, so open up that file (it should only contain two lines) and use it to
proceed through the following steps.

1. First, you'll need the "API key or Access grant" - this is on the line
   labeled `restricted key` in the text file. Copy and paste its alphanumeric
   value into the setup wizard.

2. Next, you'll need the information on the line labeled `satellite address`.
   Copy and paste this ^^entire^^ value, **including the port number** at the
   end (i.e. `7777`).

3. You'll then be asked to enter and confirm a passphrase. (As far as I can
   tell, this passphrase is only required when you open your project in the
   Storj web interface... but don't forget it!)

4. Finally, you'll be asked whether you'd like S3 backwards-compatible Gateway
   credentials. This is what we're here for, so respond with `y` and you should
   see something like this:

   ```{.console .no-copy}
   ============== GATEWAY CREDENTIALS ==============
   Access Key ID: jklasdfgh12zxcvbnm34ytrewqpo
   Secret Key   : jyuiopqwert123asdfghjkl456zxcvbnm789qwertyuiop0asdfgh
   Endpoint     : https://gateway.storjshare.io
   ```

Make sure to keep these credentials safe! They're what'll give your Mastodon
instance the ability to create and destroy objects in your Storj project, and
you definitely don't want that power to fall into the wrong hands.
:blobfox_coffee_yikes:

### Getting a link-sharing key

Storj's concept of "public buckets" differs slightly from other services. A
unique **link-sharing key** is required in order to view your files from outside
their web interface.

To generate a link-sharing key for your instance's Storj bucket, run the
following command (and **don't forget** to replace `BUCKET` with the name of
[your own bucket](#creating-a-bucket), e.g. `cutiecity`):

=== "Linux"

    ```console
    uplink share --url --readonly --disallow-lists --not-after=none sj://BUCKET
    ```

=== "macOS"

    ```console
    uplink share --url --readonly --disallow-lists --not-after=none sj://BUCKET
    ```

=== "Windows"

    ```{.console .no-copy}
    .\uplink.exe share --url --readonly --disallow-lists --not-after=none sj://BUCKET
    ```

At the end of the resulting CLI output, you should see a section that looks
similar to this:

```{.console .no-copy #linkshare-output}
================== BROWSER URL ==================
URL       : https://link.storjshare.io/s/jwcl3biyuellbunqouyj7g4htdna/cutiecity
```

<script>
  // Surround the link-sharing key with tags to make it appear as bold text.
  const span = document.querySelector("#linkshare-output span:last-child");
  const strong = document.createElement("strong");
  const keyString = span.innerHTML.match(/[a-z0-9]{28}/)[0];
  strong.appendChild(document.createTextNode(keyString));
  span.innerHTML = span.innerHTML.replace(keyString, strong.outerHTML);
</script>

Your link-sharing key is the gibberish-looking part of the URL it spits out -
mine is bolded above, as an example. This is the only piece of information you
need from the command you just ran, so feel free to ignore/discard the rest of
the output.

??? note "Note - Don't mix up your keys!"

    Just like the S3 access key you generated in the previous step, your
    link-sharing key should be **28 characters** long. Take care not to confuse
    the two! They serve different purposes and are used throughout the rest of
    this guide.

    As mentioned earlier, your **S3 access key** (when used alongside your **S3
    secret key**) effectively grants complete access to your Storj project. It's
    extremely important to keep these two keys ^^private^^.

    On the other hand, your **link-sharing key** isn't sensitive information, as
    it only allows other people to read (not write) your files in the Storj
    bucket for your Mastodon instance. In fact, if you decide to forgo the
    [last section](#linking-your-own-domain) of this guide, your link-sharing
    key will be visible in all image/video links from your instance. This is
    perfectly fine and safe! :vulpix_sparkle:

## Configuring Mastodon

Now that you have your link-sharing key and S3 credentials, it's time to plug
them all into your Mastodon production environment. :panda_science:

### Setting environment vars

Open up your `.env.production` file and configure your `S3` and `AWS` variables
as follows:

```ini title="/home/mastodon/live/.env.production"
S3_ENABLED=true
S3_PROTOCOL=https
S3_REGION=global
S3_ENDPOINT=https://gateway.storjshare.io
S3_HOSTNAME=gateway.storjshare.io
S3_BUCKET=BUCKET
S3_ALIAS_HOST=link.storjshare.io/raw/LINK_SHARING_KEY/BUCKET
AWS_ACCESS_KEY_ID=S3_ACCESS_KEY
AWS_SECRET_ACCESS_KEY=S3_SECRET_KEY
```

Make sure to replace all of the placeholders with the actual values you've
generated for them.

| Placeholder ID     | Explanation                                                                  | Example                                                              |
| ------------------ | ---------------------------------------------------------------------------- | -------------------------------------------------------------------- |
| `BUCKET`           | The name of your bucket. _(Appears twice!)_                                  | `cutiecity`                                                          |
| `LINK_SHARING_KEY` | Your link-sharing key from the [previous step](#getting-a-link-sharing-key). | `jwcl3biyuellbunqouyj7g4htdna`                                       |
| `S3_ACCESS_KEY`    | Your `Access Key ID` from the [setup wizard](#running-the-setup-wizard).     | `jklasdfgh12zxcvbnm34ytrewqpo`{#access-key}                          |
| `S3_SECRET_KEY`    | Your `Secret Key` from the [setup wizard](#running-the-setup-wizard).        | `jyuiopqwert123asdfghjkl456zxcvbnm789qwertyuiop0asdfgh`{#secret-key} |

<script>
  // Limit the width of the secret key example to maintain column proportions.
  const maxWidth = document.querySelector("#access-key").offsetWidth;
  document.querySelector("#secret-key")
    .setAttribute("style", `display: block; max-width: ${maxWidth}px`);
</script>

### Restarting the processes

Once you've finished plugging in all of those values, **save** your
`.env.production` file and then restart the relevant Mastodon processes by
executing this command:

```bash
systemctl restart 'mastodon-sidekiq' && systemctl reload 'mastodon-web'
```

You should now be able to open up your Mastodon instance in your browser and
upload images. They'll go straight to your Storj bucket and be accessible to the
public via link-sharing!

## Linking your own domain

At this point, images/videos that have been uploaded to your instance will have
fairly long URLs. For example, check out these raw URLs for [an avatar] and [a
custom emoji] from Cutie City.

If you're satisfied with those URLs, then feel free to skip this section -
you're done with this page! But if you'd like shorter ones that use your own
domain (like [this][this-avatar] or [this][this-custom-emoji]), then keep
reading. :blobhaj_read:

[an avatar]:
  https://link.storjshare.io/raw/jwcl3biyuellbunqouyj7g4htdna/cutiecity/accounts/avatars/109/867/520/496/596/492/original/a37f55905bc13d6d.png
[a custom emoji]:
  https://link.storjshare.io/raw/jwcl3biyuellbunqouyj7g4htdna/cutiecity/custom_emojis/images/000/000/046/original/f483d4f4894eb2d9.png
[this-avatar]:
  https://media.cutie.city/accounts/avatars/109/867/520/496/596/492/original/a37f55905bc13d6d.png
[this-custom-emoji]:
  https://media.cutie.city/custom_emojis/images/000/000/046/original/f483d4f4894eb2d9.png

### Designating a subdomain

The first thing you'll need to do is pick a name for the subdomain that will be
serving your images and videos. I personally chose `media` (as in
`media.cutie.city`), but you can use something like `files`, `content`, or any
other term you prefer.

After you've decided on a name, open up your `.env.production` file again and
look for this line:

```{.ini .annotate .no-copy title="/home/mastodon/live/.env.production"}
S3_ALIAS_HOST=link.storjshare.io/raw/LINK_SHARING_KEY/BUCKET # (1)!
```

1. You configured this value in an [earlier step](#configuring-mastodon), so it
   should actually look something like this:
   ```{.ini .no-copy #alias-example}
   S3_ALIAS_HOST=link.storjshare.io/raw/jwcl3biyuellbunqouyj7g4htdna/cutiecity
   ```

<style>
  /* Extra-specific styling to make the code annotation look better. */
  #alias-example span:last-child::after { content: "  "; }
  #alias-example pre { margin-top: 0.6em; margin-bottom: 0.2em; }
  .annotate code .md-annotation .md-tooltip { width: 15.65rem; }
</style>

Make sure to keep your `LINK_SHARING_KEY` and `BUCKET` on hand, because you'll
need them in the next step. Once you've copied them somewhere, replace the value
of `S3_ALIAS_HOST` with the subdomain you decided on. As an example, here's what
that line looks like in my config:

```{.ini .no-copy title="/home/mastodon/live/.env.production"}
S3_ALIAS_HOST=media.cutie.city
```

### Reverse-proxying via nginx

Now you'll need to set up a **reverse proxy** so that all requests to your
subdomain can be passed on to Storj. Since [nginx] is used in the official
[Mastodon setup instructions] and also works very nicely as a reverse proxy,
it's what I decided to use for this piece of the puzzle.

Note that Storj has recently implemented official support for [custom domains],
which solves the same problem but requires you to upgrade to a [Pro Account].
Alternatively, there are other open-source projects that also allow you to
easily set up a reverse proxy, such as [Caddy].

If you have a different preferred solution, feel free to use that instead - and
after setting it up, you can skip ahead to the next (and very last) step. But if
you'd like to use **nginx**, expand the following info box for instructions.

[nginx]: https://nginx.org
[mastodon setup instructions]:
  https://docs.joinmastodon.org/admin/install/#setting-up-nginx
[custom domains]: https://docs.storj.io/dcs/custom-domains-for-linksharing
[pro account]: https://docs.storj.io/dcs/concepts/limits
[caddy]: https://caddyserver.com/docs/quick-starts/reverse-proxy
[this article]:
  https://docs.joinmastodon.org/admin/optional/object-storage-proxy
[this thread]:
  https://forum.storj.io/t/object-storage-provider-for-mastodon-instance/11464/26
[pull request]:
  https://github.com/CutieCity/.github/blob/main/.github/contributing.md
[this page]:
  https://github.com/CutieCity/guide/blob/main/docs/self-hosting/object-storage.md
[previous step]: #designating-a-subdomain

??? info "Info - Configuring nginx"

    **Disclaimer:** I'm _far_ from an expert on nginx and only barely know
    enough about it to get this particular use case to work. The code provided
    here was cobbled together based on [this article] from the official Mastodon
    docs and [this thread] on the Storj forums. If you're more knowledgeable
    than I am (which, let's be real, is quite likely) and would like to help
    improve this guide, please don't hesitate to open a [pull request] for [this
    page]! :cat_love:

    With that said, here's an example nginx configuration that solves the
    problem at hand (and adds some nice caching):

    ```nginx linenums="1" hl_lines="4 15 23 24 41" title="/etc/nginx/sites-available/media.cutie.city"
    server {
      listen 80;
      listen [::]:80;
      server_name media.cutie.city;

      access_log /dev/null;
      error_log /dev/null;

      return 301 https://$host$request_uri;
    }

    server {
      listen 443 ssl http2;
      listen [::]:443 ssl http2;
      server_name media.cutie.city;

      ssl_protocols TLSv1.2 TLSv1.3;
      ssl_ciphers HIGH:!MEDIUM:!LOW:!aNULL:!NULL:!SHA;
      ssl_prefer_server_ciphers on;
      ssl_session_cache shared:SSL:10m;
      ssl_session_tickets off;

      ssl_certificate /etc/letsencrypt/live/media.cutie.city/fullchain.pem;
      ssl_certificate_key /etc/letsencrypt/live/media.cutie.city/privkey.pem;

      keepalive_timeout 30;

      access_log /var/log/nginx/media-access.log;
      error_log /var/log/nginx/media-error.log;

      root /var/www/html;

      location = / {
        index index.html;
      }

      location / {
        try_files $uri @s3;
      }

      set $s3_backend 'http://link.storjshare.io/raw/LINK_SHARING_KEY/BUCKET';

      location @s3 {
        limit_except GET {
          deny all;
        }

        resolver 8.8.8.8;
        proxy_set_header Host link.storjshare.io;
        proxy_set_header Connection '';
        proxy_set_header Authorization '';
        proxy_hide_header Set-Cookie;
        proxy_hide_header 'Access-Control-Allow-Origin';
        proxy_hide_header 'Access-Control-Allow-Methods';
        proxy_hide_header 'Access-Control-Allow-Headers';
        proxy_hide_header x-amz-id-2;
        proxy_hide_header x-amz-request-id;
        proxy_hide_header x-amz-meta-server-side-encryption;
        proxy_hide_header x-amz-server-side-encryption;
        proxy_hide_header x-amz-bucket-region;
        proxy_hide_header x-amzn-requestid;
        proxy_ignore_headers Set-Cookie;
        proxy_pass $s3_backend$uri;
        proxy_intercept_errors off;

        proxy_cache CACHE;
        proxy_cache_valid 200 48h;
        proxy_cache_use_stale error timeout updating http_500 http_502 http_503 http_504;
        proxy_cache_lock on;

        expires 1y;
        add_header Cache-Control public;
        add_header 'Access-Control-Allow-Origin' '*';
        add_header X-Cache-Status $upstream_cache_status;
      }
    }
    ```

    Replace `media.cutie.city` with your own domain (i.e. the **current** value
    of your `S3_ALIAS_HOST` config as set in the [previous step]) on all but one
    of the highlighted lines. Additionally, on line 41, replace
    `LINK_SHARING_KEY` and `BUCKET` with the values that **used to be** in your
    `S3_ALIAS_HOST` config.

    Save this file to `/etc/nginx/sites-available/media.cutie.city`, then enable
    it using the following commands. Make sure to replace `media.cutie.city`
    with your own domain in both the file name **and** the first command below!

    ```bash
    ln -s '/etc/nginx/sites-available/media.cutie.city' /etc/nginx/sites-enabled/
    ```

    ```bash
    systemctl reload nginx
    ```

    You'll also need an SSL certificate for your subdomain. As usual, replace
    `media.cutie.city` with your own domain:

    ```bash
    certbot certonly --nginx -d 'media.cutie.city'
    ```

    Your certificate info should be saved to `/etc/letsencrypt/live/`,
    fulfilling lines 23-24 of the configuration file. Reload nginx one more time
    before proceeding to the final step:

    ```bash
    systemctl reload nginx
    ```

### Putting it all into action

The very last thing you need to do is... restart the Mastodon processes
[again](#restarting-the-processes)!

```bash
systemctl restart 'mastodon-sidekiq' && systemctl reload 'mastodon-web'
```

Once that's done, you can open up your Mastodon instance in your browser and
admire your fancy new custom media URLs! :snuggie_dance:
