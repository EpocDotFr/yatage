from yatage.schemas import WorldSchema
import yaml

with open('examples/synacor_challenge.yml', 'r') as fp:
    sc = WorldSchema()

    print(sc.validate(yaml.safe_load(fp)))
