# Ekummat reading experience

The public site uses a shared ivory and green design in
`apps/templates/frontend/base.html` and `apps/static/frontend/ekummat/`.
No frontend build step or new runtime dependency is required.

## Content and compatibility

- Existing Quran, Hadith, library, article, admin, and API addresses are retained.
- Quran Tafseer is rendered from the original `chapter_content` HTML field.
- Hadith text continues to come from the existing Roman Urdu, Hindi, Arabic,
  reference, and grade fields. All three languages are present in the HTML;
  JavaScript adds keyboard-accessible tabs.
- Article text and citations are retained. The first article now uses the shared
  header and reading controls.
- Uploaded PDFs use their storage URL; externally hosted PDFs keep their original
  URL. No files are moved or renamed.
- Models, migrations, production settings, admin, and API behavior are unchanged.
- The homepage renders every Surah link. JavaScript initially shows twelve;
  **View all** reveals the full index, and search and filters use all 114 entries.
  Without JavaScript the complete index remains visible.
- Text size, reading theme, and a saved Surah are stored only in the reader's
  browser. The saved place is a chapter, not a paragraph or reading position.

## Local checks

With the existing Python requirements installed:

```bash
python manage.py test apps.home --settings=core.test_settings
```

The test settings use an isolated in-memory SQLite database. The tests use
representative content and mocked external requests, not the live MySQL database.

Also check the homepage, a Quran chapter containing real rich text, Hadith language
tabs, PDF links, and both article pages at desktop and phone widths. Confirm the
saved chapter and reading preferences persist in the same browser after reload.

## Publish on the existing PythonAnywhere site

Review and merge the redesign pull request before deploying. The live checkout is
`/home/awaheedp/ekummat`, its virtual environment is `ekenv`, and the web app is
`www.ekumat.com`.

1. Keep a current backup of the live database and `media/` directory in a private
   location outside the Git repository. A GitHub fork contains code and is not a
   complete backup of uploaded files or current database content.
2. In a PythonAnywhere Bash console, inspect the current checkout and preserve a
   code rollback point:

   ```bash
   cd /home/awaheedp/ekummat
   git status --short
   git branch "backup/redesign-$(date +%Y%m%d-%H%M%S)"
   ```

   Keep the existing untracked migration. Do not reset or force-push the server
   branch: it contains production settings and migration history.

3. Download and merge the reviewed changes from the fork:

   ```bash
   git fetch origin
   git merge --no-edit origin/main
   workon ekenv
   python manage.py check
   python manage.py collectstatic --noinput
   ```

   Stop if the merge, check, or static collection reports an error. Existing model
   warnings about automatic primary keys and integer `max_length` are unrelated
   to this redesign. No database migration is needed.

4. On PythonAnywhere's **Web** tab, reload **www.ekumat.com**.
5. Check the homepage, `/1/`, `/mishkat-al-masabih/`, all three PDF collections,
   `/articles/`, and `/articles/khel-ya-imtihaan/`. Test actual Hadith translations
   and open a representative PDF from each collection. Check on a phone too.

If the static assets return 404, check the static collection output and the
existing web app's static-file setup before changing settings. All new assets use
the existing `/static/` path.

## Rollback

To return to the previous presentation without touching the database, check out
the backup branch created before deployment, run `collectstatic --noinput` in
`ekenv`, and reload the web app. Preserve any later working-tree changes first.
Keep the backup branch until the redesign has been checked on the live site.
