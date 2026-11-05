FROM espocrm/espocrm:10.0.10@sha256:debf48652fed511424825839185fd67e773081ee0d665ab62cbce985acb32636

# Package the UI and supported custom application extensions into the immutable amd64 release image.
COPY custom /var/www/html/custom
COPY client/custom /var/www/html/client/custom
COPY scripts/nurivoyage /opt/nurivoyage

RUN chown -R www-data:www-data /var/www/html/custom /var/www/html/client/custom /opt/nurivoyage
