import { RmlRule } from "types/RmlRulesTypes";
import axios from "axios";
import { getBackendUrl } from "../getBackendUrl";

interface AddTripleProps {
  triple: {
    predicate: string;
    reference?: string;
    join?: {
      child: string;
      parentTriplesMap: string;
    };
  };
  rmlRule: RmlRule[];
}

export default async function addTriple({ triple, rmlRule }: AddTripleProps) {
  const url = getBackendUrl() + "/add_triple";
  const data = {
    triple,
    rml_rule: rmlRule,
  };

  const response = await axios
    .post(url, data, {
      headers: {
        "Content-Type": "application/json",
      },
    })
    .then((res) => {
      return res;
    })
    .catch((err) => {
      console.error("add triple error", err);
      return err;
    });
  return response;
}
