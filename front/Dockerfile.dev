FROM node:16
# 앱 디렉터리 (자동생성)
WORKDIR /app
# 앱 의존성
COPY package*.json ./
RUN npm install
# 앱 소스 추가
COPY . .
# 포트 설정
ENV PORT 8000
# 포트 노출
EXPOSE $PORT 
# 실행
CMD [ "npm", "run", "start"]