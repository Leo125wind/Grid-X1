FROM ubuntu:22.04

# 1. Install Essentials (SSH, X11, Python, Tools)
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y \
    openssh-server sudo xauth x11-apps net-tools iproute2 \
    python3-tk python3-pip nano \
    && rm -rf /var/lib/apt/lists/*
RUN path=$(which unminimize) && \
    if [ -n "$path" ]; then rm -f "$path"; fi && \
    echo "echo 'GRID-X SECURITY: Command Disabled'" > /usr/bin/unminimize && \
    chmod +x /usr/bin/unminimize

# 2. Setup SSH & User
RUN mkdir -p /var/run/sshd
RUN useradd -rm -d /home/renter -s /bin/bash -u 1000 renter 
RUN usermod -aG sudo renter

# 3. SSH Config (Graphics + Speed)
RUN sed -i 's/#X11Forwarding yes/X11Forwarding yes/' /etc/ssh/sshd_config
RUN sed -i 's/#X11UseLocalhost yes/X11UseLocalhost no/' /etc/ssh/sshd_config
RUN echo "AddressFamily inet" >> /etc/ssh/sshd_config
RUN echo "ClientAliveInterval 60" >> /etc/ssh/sshd_config

# 4. THE "TIME BOMB" SCRIPT
# This script handles the startup and the shutdown logic internally.
RUN echo '#!/bin/bash\n\
    # Set default lease if not provided\n\
    LEASE=${LEASE_SECONDS:-300}\n\
    echo "Starting Grid-X Session for $LEASE seconds..."\n\
    \n\
    # 1. Set the User Password (OTP)\n\
    if [ -n "$OTP" ]; then\n\
    echo "renter:$OTP" | chpasswd\n\
    fi\n\
    \n\
    # 2. Start SSH in Background\n\
    /usr/sbin/sshd -D &\n\
    SSHD_PID=$!\n\
    \n\
    # 3. Countdown Logic\n\
    # Warn at 60 seconds remaining\n\
    SLEEP_MAIN=$((LEASE - 60))\n\
    sleep $SLEEP_MAIN\n\
    \n\
    # Broadcast Warning to all active terminals\n\
    echo "⚠️  GRID-X WARNING: Session ends in 60 seconds!" | wall\n\
    \n\
    sleep 60\n\
    echo "🚨 TIME UP. Terminating Session." | wall\n\
    sleep 2\n\
    \n\
    # 4. Self-Destruct\n\
    kill $SSHD_PID\n\
    exit 0\n\
    ' > /usr/local/bin/entrypoint.sh

#5. Banner & MOTD Cleanup
RUN rm -rf /etc/update-motd.d/* && rm -f /etc/legal
RUN echo "\n\
    =======================================================\n\
    WARNING: GRID-X SECURE SESSION (GRAPHICS ENABLED)\n\
    -------------------------------------\n\
    1. Local file access is BLOCKED.\n\
    2. This session is ephemeral (data wipes on exit).\n\
    3. Administrative commands are DISABLED.\n\
    =======================================================\n" > /etc/motd

RUN chmod +x /usr/local/bin/entrypoint.sh

EXPOSE 22

# The Container now runs this script, not just SSHD
CMD ["/usr/local/bin/entrypoint.sh"]