FROM espocrm/espocrm:10.0.11@sha256:8e1c7e97e0a1a08953a86af89c3808cb95410b6a5eb487d1e3475d2c7289357d

# Package the UI and supported custom application extensions into the immutable amd64 release image.
COPY custom /var/www/html/custom
COPY client/custom /var/www/html/client/custom
COPY scripts/nurivoyage /opt/nurivoyage

RUN chown -R www-data:www-data /var/www/html/custom /var/www/html/client/custom /opt/nurivoyage
