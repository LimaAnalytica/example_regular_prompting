FROM node:16-alpine

WORKDIR /app

# Copiamos solo el package.json primero
COPY package.json ./

# Instalamos dependencias sin usar package-lock.json
RUN npm install --no-package-lock

# Copiamos el resto de los archivos
COPY . .

# Exponemos el puerto 3000
EXPOSE 3000

# Iniciamos la aplicación
CMD ["npm", "start"]