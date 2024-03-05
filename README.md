# MyForum

A forum where users can

- post articles and comments with files
- upvote\downvote on articles\comments
- followings \ followers
- messages (PM)
- informations (notifications)

## Build \ Deploy

Change your setting in `.env` file, then `docker compose up`.

```bash
# 1. Create superuser using DJANGO_SUPERUSER in .env
docker exec -it forum python ./manage.py createsuperuser --noinput

# 2. Log into the forum, go to the admin page, go to accounts, add an account link to your admin username
```

## Scrennshot

![demo1](./scrennshots/demo1.jpg)

---

![demo2](./scrennshots/demo2.jpg)
