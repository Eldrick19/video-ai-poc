def catch(msg):
    try:
        raise ValueError(msg)
    except ValueError as e:  # as e syntax added in ~python2.5
        if str(e) != "foo":
            raise
        else:
            print("caught!")