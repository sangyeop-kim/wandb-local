import re
import os
import wandb
import bcrypt
from getpass import getpass
import argparse

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("--port", "-port", type=int, default=8080)
    parser.add_argument("--container_name", "-container_name", type=str, default='wandb')

    args = parser.parse_args()

    os.makedirs('wandb', exist_ok=True)
    wandb.init(mode='offline')

    os.system(
        '''
        sudo chgrp -R 0 $(pwd)/wandb
        sudo chmod -R g+rwX $(pwd)/wandb
        sudo docker kill wandb
        sudo docker run --rm -d -v $(pwd)/wandb:/vol -p %s:8080 --name %s wandb/local
              '''
        % (args.port, args.container_name)
    )
    while True:
        email = input('\remail : ')
        result = re.findall(r'[A-z|0-9|\.]+@[a-z]+\.[a-z]+', email)

        if len(result) == 0 or result[0] != email:
            print('\r email is not valid type (ex. username@mail.com)\n email :', end='')
        else:
            break
    while True:
        password = getpass('\rpassword : ')
        password_again = getpass('password again : ')

        passwordSalt = bcrypt.gensalt(rounds=10)
        password = bcrypt.hashpw(password.encode('utf-8'), passwordSalt)
        password_again = bcrypt.hashpw(password_again.encode('utf-8'), passwordSalt)

        if password == password_again:
            os.system(
                '''sudo docker exec %s sudo sh -c "echo '%s:%s' > /vol/env/users.htpasswd" '''
                % (args.container_name, email, password.decode('utf-8').replace('$', '\$'))
            )
            break

        else:
            print('\rpassword is not same\npassword : ', end='')
