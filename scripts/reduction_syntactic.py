from biodivine_aeon import *
import argparse
import pathlib


def update_function_weight(update: UpdateFunction) -> int:
	if update is None or update.is_const() or update.is_var():
		return 1
	if update.is_param():
		raise RuntimeError("Uninterpreted functions not allowed.")
	if update.is_not():
		return 1 + update_function_weight(update.as_not())
	if update.is_binary():
		data = update.as_binary()
		return 1 + update_function_weight(data[1]) + update_function_weight(data[2])
	raise RuntimeError("Unrecognized function:", update)

def find_best_variable(bn: BooleanNetwork, max_product: int) -> VariableId | None:
	minimal_function_size: int = 0
	minimal_variable: VariableId | None = None
	for var in bn.variables():
		if var in bn.successors(var):
			continue	# Cannot reduce, self-regulation.
		
		product = len(bn.successors(var)) * len(bn.predecessors(var))
		if product > max_product:
			continue	# Cannot reduce, too dense.
		
		weight = update_function_weight(bn.get_update_function(var))
		if minimal_variable is None or weight < minimal_function_size:
			minimal_variable = var
			minimal_function_size = weight

	return minimal_variable


def main():
	parser = argparse.ArgumentParser(
		description="Perform syntactic reduction on a Boolean network."
	)
	parser.add_argument(
		"--max-product",
		type=int,
		required=True,
		help="Maximum product of successors and predecessors for reduction"
	)
	parser.add_argument(
		"--input",
		type=str,
		required=True,
		help="Path to input Boolean network file"
	)
	parser.add_argument(
		"--output",
		type=str,
		required=True,
		help="Path where the reduced network should be saved"
	)
	
	args = parser.parse_args()
	
	max_product = args.max_product
	print("Max. product:", max_product)
	
	bn = BooleanNetwork.from_file(args.input)
	print("Before reduction:", bn)
	
	while True:
		best_var = find_best_variable(bn, max_product)
		
		if best_var is None:
			break
		
		name = bn.get_variable_name(best_var)
		bn = bn.inline_variable(best_var, repair_graph=False)
		print(f"Reduced {name}:", bn)
	
	is_still_reducible = False
	for var in bn.variables():
		if var not in bn.successors(var):
			is_still_reducible = True
	
	if is_still_reducible:
		print("Exceeded max product limit.")
	else:
		print("Network is maximally reduced.")
	
	pathlib.Path(args.output).write_text(bn.to_bnet())
	print(f"Reduced network saved to: {args.output}")


if __name__ == "__main__":
	main()