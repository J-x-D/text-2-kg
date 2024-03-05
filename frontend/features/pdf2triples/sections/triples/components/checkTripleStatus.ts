import { RDFResource } from "features/pdf2triples/types/triple";

export type CheckTripleErrorType = "NO_PREDICATE" | "DUPLICATE_SUBJECT";

type HasError = {
  hasError: true;
  errorType: CheckTripleErrorType;
};

type NoError = {
  hasError: false;
};

export type CheckTripleErrorState = HasError | NoError;

export default function checkTripleErrorState(
  triples: RDFResource[],
  index: number,
): CheckTripleErrorState {
  const triple = triples[index];
  if (!triple) return { hasError: false };

  return {
    hasError: false,
  };
}
