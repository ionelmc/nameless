#!/bin/bash
set -euo pipefail
shopt -s extglob
declare -A services
docker --version
docker compose version

if [ -z "$RELOADER_MONITOR" ]; then
    echo -e "\033[1;33m[$(date -Iseconds)] Reloader is disabled. Exiting ...\033[0m"
    exit 0
fi

while true; do
    echo -e "\033[1;32m[$(date -Iseconds)] Waiting for changes ...\033[0m"
    while read event; do
        set +x
        echo -e "\033[1;36m[$(date -Iseconds)] Detected $event changes.\033[0m "
        if [[ $event =~ .*/static(/|$) ]]; then
            echo -e "\033[1;34m[$(date -Iseconds)] Running collectstatic ..."
            (
                set -x
                docker exec ${COMPOSE_PROJECT_NAME}_web_1 pysu app django-admin collectstatic --no-input -v0
            ) || echo -e "\033[1;31m[$(date -Iseconds)] Failed to run collectstatic!"
        else
            echo -e "\033[1;34m[$(date -Iseconds)] Attempting restarts ..."
            for name in $(docker compose ps --services | egrep "$RELOADER_CONTAINERS"); do
                services[$name]=1
            done
            if [[ -z "${!services[*]}" ]]; then
                echo -e "\033[1;31m[$(date -Iseconds)] No services detected. Perhaps you meant to meant to run more than just the reloader? Try using:"
                echo -e "\033[1;33m
      docker compose up reloader web

Or just run everything:

      docker compose up"
                exit 1
            fi
            echo -e "\033[1;34m[$(date -Iseconds)] Restarting ${#services[@]} services: ${!services[@]}"
            pids=()
            for name in "${!services[@]}"; do
                (
                    if [[ "$name" = web && -p /var/app/run/uwsgi.fifo ]]; then # check if the pipe exists
                        # and it actually has something connected to it
                        # (/bin/echo stuff <>path >path would get SIGPIPE if that pipe is dead)
                        echo + echo r > /var/app/run/uwsgi.fifo
                        /bin/echo r 1<>/var/app/run/uwsgi.fifo >/var/app/run/uwsgi.fifo || docker compose restart web
                    else
                        set -x
                        docker compose restart "$name"
                    fi
                ) &
                pids+=($!)
            done
            wait "${pids[@]}"
        fi
    done < <(
        set -x
        fswatch \
            --recursive \
            --extended \
            --exclude '\.git|__pycache__|\.pyc|\.egg-info|___jb_|\..+~$' \
            --event Created \
            --event Updated \
            --event Removed \
            --event Renamed \
            --event OwnerModified \
            --event AttributeModified \
            --event MovedFrom \
            --event MovedTo \
            --one-per-batch \
            --monitor ${RELOADER_MONITOR:-inotify}_monitor \
            /app/src/
    )
done
