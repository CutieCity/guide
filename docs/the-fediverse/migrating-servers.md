# Migrating Servers

Because the Fediverse is decentralized and each of its servers is independently
owned/managed, there's a non-zero chance that at some point, you'll find
yourself wanting (or needing) to migrate your account to a different server.
This may be because you've found one that aligns better with your desired social
media experience, because your current server is shutting down, or any other
reason. It isn't a bad thing - and fortunately, migrating to another server is
easier than it sounds.

On this page, I'll walk you through the migration process from one [Mastodon]
instance to another. According to [Fediverse Observer], Mastodon's user base
makes up around **80%** of the Fediverse, so hopefully this is useful for you.
If you're knowledgeable about the migration process to/from a different kind of
server and would like to contribute to this guide, please don't be shy to open a
[pull request] for [this page]! :birb_heart:

[mastodon]: https://joinmastodon.org
[fediverse observer]: https://fediverse.observer/stats
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

    This is the primary functionality provided by Mastodon's built-in account
    migration tool. As soon as you press the **Move Followers** button, a number
    of background processes across the Fediverse will start to update your
    accounts' relationships. Your followers will automatically unfollow your
    current account and follow your new one in its place, without any action
    needed on their part. Some of them might not even notice the change!

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

??? info "None of your other data will be transferred automatically."

    As mentioned above, you'll need to explicitly transfer the list of **users
    that you follow** (unless you're looking to start from scratch with an empty
    home timeline). You may also want to download and transfer your current
    account's **bookmarks**, **muted users**, **blocked users**, and **blocked
    domains**.

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
??? info "After migrating, there is a 30-day waiting period during which you will not be able to migrate again."

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
    the migration process from your account on **Server B** whenever you want,
    and you'll take all 69 of your lovely followers with you (again).

    Big thanks to [Yona] for spreading the word about this! :heart_trans:

<!-- prettier-ignore -->
??? info "Your current account's profile will be updated with a redirect notice and be excluded from searches."

    Although this point is largely self-explanatory, it's worth mentioning that
    your current (i.e. old) account will be unable to gain new followers while
    the redirect notice is in place (or permanently, if you have no intention
    of ever returning to that account and taking down the notice). This makes
    sense, because following an abandoned shell of an account doesn't make for a
    great user experience. :blobfox_trash_derp:

??? info "Your current account will not be fully usable afterwards. However..."

    ... you _will_ have access to **data export** and **re-activation**.
    This means that it's totally fine if you accidentally press the **Move
    Followers** button before downloading your account archive and/or any
    accompanying files (i.e. bookmarks, blocks, etc). You'll still be able to
    log in to retrieve those things during/after the migration process.
    Additionally, the option to migrate back to your current account will remain
    available (unless its server is shutting down, of course).

    What you _won't_ be able to do, however, is update your **profile** or any
    **posts** on the account you've migrated from - so make sure you clean those
    things up (as much as you feel is necessary) before hitting the magic
    button! :robot_headpats:

If all of those things sound acceptable to you, let's get started! :cat_wizard:

[account migration]: https://docs.joinmastodon.org/user/moving/#move
[boost]: https://tech.lgbt/@Natasha_Jay/109643276422036265
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
          type="text"
        />
      </div>
      <div class="custom-account input-field">
        <label for="new_account">New Account</label>
        <input
          id="new_account"
          class="md-input md-input--stretch"
          placeholder="@yourname@cutie.city"
          type="text"
        />
      </div>
    </div>

    **Note:** The values you put in won't be saved or sent anywhere outside this
    page. They'll only be accessed by some very basic client-side Javascript
    code in order to customize the placeholder text and links below.

[fedi.garden]: https://fedi.garden
[cutie.city]: https://cutie.city/about

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
containing the text "Create Alias" in all-capitalized letters.")

<style>
  /* Remove extraneous spacing below the "Create Alias" image. */
  #creating-an-account-alias + * + p { line-height: 0; }
</style>

=== "Default Instructions"

    Put the full handle of your <u>old</u> account
    (e.g. **@yourname@mastodon.social**) into the text box,
    then click the **Create Alias** button.

=== "Customized Instructions"

    Put your <u>old</u> handle (<strong data-custom-text="@OLD_HANDLE">
    </strong>) into the text box, then click the **Create Alias** button.

After the operation finishes, you should see this message at the top of the
page:

> Successfully created a new alias. You can now initiate the move from the old
> account.

## More info coming soon!
