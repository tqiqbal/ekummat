# Publishing articles

Articles are HTML templates stored in `apps/templates/frontend/articles/`.
The public index is `/articles/`. The first article, **Khel Ya Imtihaan**,
is available at `/articles/khel-ya-imtihaan/`.

## Add another article

1. Place the HTML file in `apps/templates/frontend/articles/` with a lowercase,
   hyphenated filename. A complete HTML document can keep its own CSS and layout.
2. Add a `TemplateView` route in `apps/home/urls.py`, following the first article's
   route. Give each route a unique URL and name.
3. Add a card to `apps/templates/frontend/articles/index.html` with the article's
   title, topic, description, and a link using its named URL.
4. Include links back to the site and the article index in the article. The first
   article demonstrates these links without changing its original content.
5. Commit and merge the changes, then deploy them to PythonAnywhere.

These pages are published when deployed; they are not managed in Django admin.
Only add reviewed HTML from trusted authors, as templates may contain scripts
and Django template tags.

## Deploy on PythonAnywhere

After merging the pull request, open a Bash console for the existing project:

```bash
cd /home/awaheedp/ekummat
git status --short
git pull --ff-only origin main
workon ekenv
python manage.py check
```

Keep any existing local changes. If Git reports a conflict or Django reports an
error, resolve it before reloading the site. This article change needs no database
migration or new Python packages.

On the **Web** tab, select **www.ekumat.com** and click **Reload**. Check:

- `/articles/` lists the article.
- `/articles/khel-ya-imtihaan/` displays the complete article.
- The homepage menu contains **Articles**, including on a narrow screen.
- The article's **All articles** and **Ekummat** links work.
