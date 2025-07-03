# 🎵 LuteMusic Django Auto-Environment Setup

This project uses automatic environment activation to avoid manually activating the virtual environment every time.

## How It Works 🚀

**Automatically activates when you `cd` into the directory**

The project uses [direnv](https://direnv.net/) to automatically:
- Activate the Python virtual environment
- Set Django environment variables  
- Configure the Python path

## Setup Instructions

### 1. Install direnv:
```bash
# macOS
brew install direnv

# Add to your shell config (~/.zshrc or ~/.bashrc)
eval "$(direnv hook zsh)"  # for zsh
eval "$(direnv hook bash)" # for bash
```

### 2. Allow the .envrc file:
```bash
direnv allow
```

### 3. That's it! 
Now whenever you `cd` into this directory, the environment auto-activates.

## 🎯 Your Workflow

```bash
# Navigate to project
cd ~/Sites/lutemusic.v2
# 🎵 Auto-activates: virtual env + Django settings

# Use standard Django commands
python manage.py runserver       # Start development server
python manage.py createsuperuser # Create admin user  
python manage.py startapp music  # Create new app
python manage.py makemigrations  # Create migrations
python manage.py migrate         # Apply migrations
python manage.py shell           # Django shell
python manage.py test            # Run tests
```

## 🔧 Environment Variables Set

- `DJANGO_SETTINGS_MODULE=config.settings`
- `DJANGO_DEBUG=True`
- `PYTHONPATH` includes project root
- `VIRTUAL_ENV` points to the venv

---

**🎉 Enjoy automatic environment activation!** 