from biodivine_aeon import *
import argparse
import pathlib

def get_regulator_dict(stg: AsynchronousGraph) -> dict[[VariableId, set[BddVariable]]]:
    return { var: stg.mk_update_function(var).support_set() for var in stg.network_variables() }

def get_network_weight(stg: AsynchronousGraph) -> int:
    result = 0
    for var in stg.network_variables():
        result += stg.mk_update_function(var).node_count()
    return result

def find_best_variable(stg: AsynchronousGraph, max_product: int) -> VariableId | None:
    minimal_function_size: int = 0
    minimal_variable: VariableId | None = None
    regulators = get_regulator_dict(stg)
    for var in stg.network_variables():
        sym_var = stg.symbolic_context().find_network_bdd_variable(var)
        if sym_var in regulators[var]:
            continue	# Cannot reduce, self-regulation.
    
        product = len(regulators[var]) * sum(1 for x in stg.network_variables() if sym_var in regulators[x])
        if product > max_product:
            continue	# Cannot reduce, too dense.
        
        update = stg.mk_update_function(var)
        weight = update.node_count()
        if minimal_variable is None or weight < minimal_function_size:
            minimal_variable = var
            minimal_function_size = weight
            
    return minimal_variable


def main():
    parser = argparse.ArgumentParser(
        description="Perform symbolic reduction on a Boolean network."
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
    stg = AsynchronousGraph(bn)
    
    while True:
        best_var = find_best_variable(stg, max_product)
        
        if best_var is None:
            break
        
        name = stg.get_network_variable_name(best_var)
        stg = stg.inline_variable_symbolic(best_var)
        stg_weight = get_network_weight(stg)
        print(f"[{stg_weight}] Reduced {name}:", stg.network_variable_count())
        
    regulators = get_regulator_dict(stg)
    is_still_reducible = False
    for var in stg.network_variables():
        sym_var = stg.symbolic_context().find_network_bdd_variable(var)
        if sym_var not in regulators[var]:
            is_still_reducible = True
            
    if is_still_reducible:
        print("Exceeded max product limit.")
    else:
        print("Network is maximally reduced.")
        
    pathlib.Path(args.output).write_text(stg.reconstruct_network().to_bnet())
    print(f"Reduced network saved to: {args.output}")


if __name__ == "__main__":
    main()