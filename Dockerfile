FROM librenms/librenms:latest

RUN apk --update --no-cache add iperf3 py3-pip
RUN pip3 install iperf3 --break-system-packages

RUN mkdir -p /opt/librenms/includes/html/graphs/services/
COPY check_iperf3.inc.php /opt/librenms/includes/html/graphs/services/check_iperf3.inc.php
RUN chown librenms:librenms /opt/librenms/includes/html/graphs/services/check_iperf3.inc.php \
    && chmod 644 /opt/librenms/includes/html/graphs/services/check_iperf3.inc.php
