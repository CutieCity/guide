# Migrating Servers

Because the Fediverse is [decentralized] and each of its servers is
independently owned/managed, there's a non-zero chance that at some point,
you'll find yourself wanting (or needing) to migrate your account to a different
server. This may be because you've found one that aligns better with your
desired social media experience, because your current server is shutting down,
or for any other reason. It isn't a bad thing - and fortunately, migrating is
easier than it may seem!

On this page, I'll walk you through the migration process from one [Mastodon]
instance to another. According to [Fediverse Observer], Mastodon's user base
makes up around **80%** of the Fediverse, so hopefully this is useful for you.
If you're knowledgeable about the migration process to/from a different kind of
server (such as [Misskey] or [Akkoma]) and would like to contribute to this
guide, feel free to open a [pull request] for [this page]! :birb_heart:

[decentralized]:
  https://fedi.tips/why-is-the-fediverse-on-so-many-separate-servers
[mastodon]: https://joinmastodon.org
[fediverse observer]: https://fediverse.observer/stats
[misskey]: https://misskey-hub.net
[akkoma]: https://akkoma.social
[pull request]:
  https://github.com/CutieCity/.github/blob/main/.github/contributing.md
[this page]:
  https://github.com/CutieCity/guide/blob/main/docs/the-fediverse/migrating-servers.md

## Understanding the process

Although migrating is fairly easy, it's important to make sure that it's what
you _actually_ want to do, as it does bear some caveats that you should fully
understand before initiating the process. You'll see a brief summary of these
points on Mastodon's [Account Migration] page, but I've reproduced them below in
order to clarify and thoroughly explain each one. (Click to expand the boxes!
:cat_lurk:)

<!-- prettier-ignore -->
??? info "All of your followers will be transferred from your current account to your new account."
    <a id="understanding-the-process-1"></a>

    This is the main functionality provided by Mastodon's built-in account
    migration feature. As soon as you press the **Move Followers** button, a
    number of background processes across the Fediverse will start to update
    your accounts' relationships. Your followers will automatically unfollow
    your current account and follow your new one in its place, without any
    action required on their part. Some of them might not even notice the
    change!

    Depending on how busy your followers' home servers currently are, these
    updates may take anywhere from a few seconds to a few hours (or even days,
    although it's rare for servers to be _that_ slow). This is only a tiny
    inconvenience, as your new account will be otherwise fully functional and
    you can continue to use it while waiting for any stragglers.

    **Note:** This automatic process only transfers your **Followers** list
    (i.e. the users that follow you) - _not_ your **Following** list (i.e. the
    users that you follow)! The latter will need to be manually exported from
    your current account, then imported into your new account (but don't worry,
    these steps are quick and easy).

<!-- prettier-ignore -->
??? info "None of your other data will be transferred automatically."
    <a id="understanding-the-process-2"></a>

    As mentioned above, you'll need to explicitly transfer the list of **users
    that you follow** (unless you're looking to start from scratch with an empty
    home timeline). You may also want to [download] and [transfer] your current
    account's **bookmarks**, **muted users**, **blocked users**, and **blocked
    domains**. We'll go into detail about those steps later!

    Unfortunately, there's currently no way to automatically copy over the
    **posts** (a.k.a. **toots**) that you've made from your current account. You
    may wish to [boost] some of them from your new account to preserve your post
    history (if that's something you're interested in) and/or to establish your
    new timeline. Ideally, this should be done _before_ transferring your
    followers to your new account, in order to avoid flooding their home
    timelines with your old posts - unless that's actually something you _want_
    to do. :cat_welp:

    **Note:** Boosting your old posts is _not_ an effective strategy if your
    current instance is shutting down. Once the instance goes offline for good,
    your old posts (and any boosts thereof) will disappear along with it.
    Instead of boosting them, you'll have to manually re-post them on your new
    account if you feel strongly about preserving your post history.

<!-- prettier-ignore -->
??? info "Your new account must first be configured to back-reference your current one."
    <a id="understanding-the-process-3"></a>

    This point is simply emphasizing a prerequisite step ([Creating an
    account alias]) that you'll need to complete on your new server before
    initiating the account migration from your current server. This guide
    will cover all of the necessary migration steps in order (and in great
    detail :sparkles_autistic:) - so don't worry too much about accidentally
    messing things up!

<!-- prettier-ignore -->
??? info "After migrating, there is a 30-day waiting period during which you won't be able to migrate again."
    <a id="understanding-the-process-4"></a>

    This caveat is often misunderstood, and isn't actually as restrictive as it
    sounds. It's true that a "cooldown" period begins when you press the **Move
    Followers** button, preventing you from doing so again for the following 30
    days. However, this limitation is applied to your current (i.e. old,
    obsolete) account, _not_ to your new one! :shark_pog:

    To illustrate this with an example, let's say you've decided to move from
    **Server A** to **Server B**. You press the magic button, go to bed, and
    wake up the next day to find that all 69 of your followers have successfully
    been transferred to your new account on **Server B**. Yay! But wait - you
    also notice a brand-new announcement on **Server B** stating that anyone who
    posts spoilers about a certain game will be swiftly banned... and you were
    _so_ excited to post about how Professor Fig dies and Rookwood cursed Anne!
    :frog_cry: Clearly, **Server B** isn't as great of a place as you thought it
    was. But you've only _just_ arrived, so does that mean your account is stuck
    there for 30 days?

    Luckily, the answer to that question is **no**! Only _one_ of your accounts
    is affected by the cooldown period, and it's the old one on **Server A** -
    not that there would be much of a point in migrating that account again, as
    it no longer has any of your followers attached to it. You're free to begin
    the migration process from your account on **Server B** as soon as you want
    to, and you'll take all 69 of your lovely followers with you (again).

    Big thanks to [Yona] for spreading the word about this! :heart_trans:

<!-- prettier-ignore -->
??? info "Your current account's profile will be updated with a redirect notice and be excluded from searches."
    <a id="understanding-the-process-5"></a>

    Although this point is largely self-explanatory, it's worth mentioning that
    your current (i.e. old) account will be unable to gain new followers while
    the redirect notice is in place (or permanently, if you have no intention
    of ever returning to that account and taking down the notice). This makes
    sense, because following an abandoned shell of an account doesn't make for a
    great user experience. :blobfox_trash_derp:

<!-- prettier-ignore -->
??? info "Your current account won't be fully usable after you migrate away from it. However..."
    <a id="understanding-the-process-6"></a>

    ... you _will_ have access to **data export** and **re-activation**.
    This means that it's totally fine if you accidentally press the **Move
    Followers** button before downloading your account archive and/or any
    accompanying files (i.e. bookmarks, blocks, etc). You'll still be able to
    log in to retrieve them during/after the migration process. Additionally,
    the option to migrate back to your current account will remain available
    (unless your current server is shutting down, of course).

    What you _won't_ be able to do, however, is update your **profile** or any
    **posts** on the account you've migrated from - so make sure you clean those
    things up (as much as you feel is necessary) before hitting the magic
    button! :robot_headpats:

If all of those things sound acceptable to you, let's get started! :cat_wizard:

[account migration]: https://docs.joinmastodon.org/user/moving/#move
[download]: #exporting-your-data
[transfer]: #importing-your-data
[boost]: https://tech.lgbt/@Natasha_Jay/109643276422036265
[creating an account alias]: #creating-an-account-alias
[yona]: https://eldritch.cafe/@yonabee/109906208870346342

## Plotting your course

The first step in the migration process is, of course, designating your desired
destination. If you haven't decided which server to make your new home, check
out the nicely-curated selection of servers listed on [Fedi.Garden]. And I may
be a little bit biased, but I hear [cutie.city] is one of the best servers in
the entire Fediverse! :flareon_wink:

Once you've selected a server and created your new account, you're ready to
begin your journey.

???+ tip "Tip - Customize this guide!"

    Do you want personalized instructions and direct links to all of the pages
    you'll need to visit during this process? :rainbow_creature: If so, fill out
    these two fields with your own usernames:

    <div class="grid">
      <div class="custom-account input-field">
        <label for="old_account">Old Account</label>
        <input
          id="old_account"
          class="md-input md-input--stretch"
          placeholder="@yourname@mastodon.social"
          pattern="^\s*@?\w+@[a-zA-Z0-9]+([-.][a-zA-Z0-9]+)*\.[a-zA-Z]{2,}\s*$"
          autocomplete="off"
          type="text"
        />
        <span />
      </div>
      <div class="custom-account input-field">
        <label for="new_account">New Account</label>
        <input
          id="new_account"
          class="md-input md-input--stretch"
          placeholder="@yourname@cutie.city"
          pattern="^\s*@?\w+@[a-zA-Z0-9]+([-.][a-zA-Z0-9]+)*\.[a-zA-Z]{2,}\s*$"
          autocomplete="off"
          type="text"
        />
        <span />
      </div>
    </div>

    **Note:** The values you put in won't be saved or sent anywhere outside this
    page. They'll only be accessed by some very basic [client-side JavaScript
    code] in order to customize the instructions and links below.

[fedi.garden]: https://fedi.garden
[cutie.city]: https://cutie.city/about
[client-side javascript code]:
  https://github.com/CutieCity/guide/blob/main/docs/javascripts/migrating-servers.js

## Creating an account alias

=== "Default Instructions"

    On your <u>new</u> account, go to **Preferences** > **Profile**. Scroll down
    to the bottom of the page and look for the section called **Moving from a
    different account**. Follow the link to **create an account alias**.

    On that page, you should see a form that looks like this:

=== "Customized Instructions"

    Go to the <a data-custom-link="http://NEW_SERVER/settings/aliases">Account
    Aliases</a> page on your <u>new</u> server. You should see a form that looks
    like this:

![](/images/migrating-servers_create-alias.png "A screenshot of the relevant
section on the aforementioned page. There's a required text box labeled "Handle
of the old account", with a hint saying to "Specify the username@domain of the
account you want to move from". Below the text box, there's a large button
containing the text "Create Alias" in all-capitalized letters."){.no-lightbox}
{style="line-height: 0;"}

=== "Default Instructions"

    Put the full handle of your <u>old</u> account
    (e.g. **@yourname@mastodon.social**) into the text box,
    then click the **Create Alias** button.

=== "Customized Instructions"

    Put your <u>old</u> handle (<strong data-custom-text="@OLD_HANDLE">
    </strong>) into the text box, then click **Create Alias**.

When the operation finishes, you should see a message that says something like
this:

> Successfully created a new alias. You can now initiate the move from your old
> account.

It may take a few minutes for your old server to become aware of the new alias,
so let's tackle another migration step while that happens in the background!

## Exporting your data

=== "Default Instructions"

    On your <u>old</u> account, go to **Preferences** > **Import and export**.
    You should see a table like this:

=== "Customized Instructions"

    Go to the <a data-custom-link="http://OLD_SERVER/settings/export">Data
    Export</a> page on your <u>old</u> server. You should see a table that looks
    like this:

<!-- prettier-ignore -->
![](/images/migrating-servers_export-data.png "A screenshot of the relevant
section on the aforementioned page. It contains a table with rows labeled
"Media storage", "Posts", "Follows", "Lists", "Followers", "You block",
"You mute", "Domain blocks", and "Bookmarks". Most of the rows (all except
for "Media storage", "Posts", and "Followers"\) provide a link to download
a CSV file."){.no-lightbox}
{style="line-height: 0;"}

With the sole exception of [Lists], all table rows containing a
<span id="csv">":fa_solid_download: **CSV**"</span> link can be transferred to
your new account via a mostly-automated process. Click the links to download the
`.csv` files for the items that you'd like to take with you to your new account.

<style>
  /* Extra-specific styling to make the CSV text, icon, and code look better. */
  #csv { margin: 0 0.1em; white-space: nowrap; }
  #csv > .twemoji { margin-right: 0.05em; width: 0.9em; }
  #csv ~ code { margin: 0 0.1em; padding: 0 0.5em 0 0.3em; }
</style>

??? tip "Tip - Decide which data is worth transferring!"

    Here are some opinions/recommendations on which pieces of data are worth
    transferring over to your new server, based on my own personal experience:

    - [x] **Follows** - Definitely. If you aren't following lots of accounts,
          then you probably aren't very well-Fediversed. :sip_tea:
    - [ ] **You block** - Only if you think these users will continue being
          problematic (probably worth checking manually).
    - [ ] **You mute** - Same as the above point about your blocked users.
    - [ ] **Domain blocks** - Only if you block a lot of domains that aren't
          already blocked by your new server.
    - [x] **Bookmarks** - Recommended if you have lots of bookmarks that you
          want to continue being able to access.

    **Note:** The above checkboxes are toggleable, which may be helpful if you
    decide to go with a different subset of data and/or want to keep track of
    the things that you'll need to [import] into your new account!

??? question "FAQ - What about the rows without a CSV link?"

    If you'd like to download your **posts** and any **media** that you've
    uploaded to your current account, you can do so by clicking the **"Request
    your archive"** button, which you'll find below the table pictured in the
    above screenshot (unless you've already clicked it within the past week).
    You won't be able to transfer this data to your new account - at least not
    with any official tools - unless you want to re-post it all manually.
    :psyduck_sweat: Regardless, it can be nice to have a copy of your posts and
    uploads, especially if your current server is shutting down.

    As for your **followers**, we'll be moving them over to your new account in
    the [next step]!

[lists]: https://github.com/mastodon/mastodon/issues/15015
[import]: #importing-your-data
[next step]: #migrating-your-followers

## Migrating your followers

Coming soon!

## Importing your data

Coming soon!
