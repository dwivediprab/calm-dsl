'''
Sample single vm example to convert python dsl to calm v3 api spec

'''

import json

from scratch import Service, Substrate, Deployment, Profile, Blueprint



class MySQL(Service):

    def __init__(self):
        super().__init__()
        self.foo = "foo"
        self.bar = "bar"


class AHVMedVM(Substrate):

    def __init__(self):
        # TODO: load super automatically in metaclass
        super().__init__()


class MySQLDeployment(Deployment):

    def __init__(self):
        super().__init__()
        self.add_substrate(AHVMedVM())
        self.add_service(MySQL())


class NxProfile(Profile):

    def __init__(self):
        super().__init__()
        self.add_deployment(MySQLDeployment())



class MyBlueprint(Blueprint):
    """sample bp description"""

    def __init__(self):
        super().__init__()
        self.add_profile(NxProfile())



def main():

    bp = MyBlueprint()
    dct = dict()
    out = bp.dump(dct)
    print(json.dumps(out))


if __name__ == "__main__":
    main()