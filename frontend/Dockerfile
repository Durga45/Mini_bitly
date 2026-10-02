# Official Nginx lightweight image lo
FROM nginx:alpine

# Apne index.html ko Nginx ke default public folder me copy karo
COPY index.html /usr/share/nginx/html/index.html

# Nginx config copy karo (optional, but standard practice)
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Port 80 expose karo
EXPOSE 80

# Nginx ko foreground me start karo
CMD ["nginx", "-g", "daemon off;"]