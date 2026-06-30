# Deploying nickomara.com

Three steps: **push** the site to GitHub, **enable** GitHub Pages, **point** your domain at it.

---

## 1. Push the site to GitHub

From the repo folder in Terminal:

```bash
cd "/Users/Nick/Google_Drive/Professional Development/Personal Website/nomara_prof_website"
git add .
git commit -m "Build initial website"
git push
```

### If git asks you to authenticate
GitHub no longer accepts your account password on the command line. Easiest fix — install the
GitHub CLI once and sign in:

```bash
brew install gh        # if you don't have Homebrew, see https://brew.sh
gh auth login          # choose: GitHub.com → HTTPS → login with a browser
```

Then re-run the `git push` above. (Alternatively, create a Personal Access Token at
GitHub → Settings → Developer settings → Tokens, and use it as the password when prompted.)

---

## 2. Enable GitHub Pages

1. Go to **https://github.com/nickomara/nomara_prof_website**
2. **Settings → Pages**
3. Under **Build and deployment**, set **Source = "Deploy from a branch"**,
   **Branch = `main`**, **Folder = `/ (root)`**, then **Save**.
4. In a minute the site goes live at `https://nickomara.github.io/nomara_prof_website/`.

---

## 3. Point nickomara.com at GitHub Pages

Your domain is registered through **WordPress.com**, so you'll edit its DNS records there.

1. WordPress.com → **Upgrades → Domains → nickomara.com → DNS records**
   (or go to `https://wordpress.com/domains/manage/nickomara.com/dns/nickomara.com`).
2. Remove the existing A records that point the apex (`@`) at WordPress, then **add these four
   A records** for the root domain (`@`):

   ```
   185.199.108.153
   185.199.109.153
   185.199.110.153
   185.199.111.153
   ```

3. Add a **CNAME** record so `www` works:

   ```
   Name: www    Value: nickomara.github.io
   ```

4. Back on GitHub → **Settings → Pages → Custom domain**, enter **`nickomara.com`** and Save.
   (The `CNAME` file in this repo already declares it.) Once the check passes, tick
   **Enforce HTTPS**.

DNS changes can take anywhere from a few minutes to a few hours to propagate. After that,
**https://nickomara.com** serves this site.

> Once the new site is confirmed working, you can cancel the WordPress.com plan and keep only
> the domain registration — there's nothing left for WordPress to host.

---

## Day-to-day updates

Edit a file, then:

```bash
git add .
git commit -m "what you changed"
git push
```

The live site updates within ~1 minute. To update your CV, just replace
`assets/files/Nicholas_OMara_CV.pdf` (same filename) and push.
