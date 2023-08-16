# IMGenie FrontEnd

### 1️⃣ Install packages

```bash
npm i
```

### 2️⃣ Build & Execute server

```bash
npm run build
npx serve -s build -l [port number]
```

### 🐳 Build docker image

```bash
# dev
docker build -f Dockerfile.dev -t username:tag
# prod
docker build -f Dockerfile.prod -t username:tag
```
