# RFComm

Very simple RFComm, implemented in Python3, that is used to grab data from BT and write it to InfluxDB.

## Prerequisites

```console
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
```

## How to run

Install the [file](rfcomm.service) in your systemd compatible system and execute:

```console
sudo systemctl enable rfcomm
sudo systemctl start rfcomm
sudo systemctl status rfcomm
```

## Authors

* **Mário Antunes** - [mariolpantunes](https://github.com/mariolpantunes)

## License

This project is licensed under the MIT License - see the [LICENSE.md](../LICENSE.md) file for details