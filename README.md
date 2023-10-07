# Mathbridge (Open-source Demo) 
Machine learning, data, and statistics visualization website for Virginia Tech CS department. The full source code is not public, however, the published website can be found [here](https://mathbridge.discovery.cs.vt.edu/)

![](https://raw.githubusercontent.com/mnguyen0226/mnguyen0226.github.io/main/content/posts/mathbridge/imgs/mathbridge_architecture.png)

## Reproduce Project
1. Clone Repository
```sh
https://github.com/mnguyen0226/mathbridge_official.git
cd mathbridge_official
```

2. Create Virtual Environment
```sh
pip install virtualenv
virtualenv venv
python3 -m venv venv

# for Linux
source venv/bin/activate

# for Window
.\venv\Scripts\activate
```

3. Install Packages
```sh
pip install -r requirements.txt
pip install gunicorn
```

4. Run Project
```
chmod +x run.sh
./run.sh
```
