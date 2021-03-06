import os

class LazyFormatter:
	def __init__(self, valobj, dict):
		self.valobj = valobj

	def get_child_index(self, name):
		return 0 # There is only ever one child

	def num_children(self):
		if self.has_value:
			return 1
		return 0
	
	def get_child_at_index(self, index):
		if index != 0:
			return None # There is only ever one child
		if not self.has_value:
			return None
		
		value = (self.valobj
			.GetChildMemberWithName('value_')
			.GetChildMemberWithName('storage_')
			.GetChildMemberWithName('value')
		)

		return value
	
	def update(self):
		self.has_value = True if (self.valobj
			.GetChildMemberWithName('value_')
			.GetChildMemberWithName('storage_')
			.GetChildMemberWithName('hasValue')
			.GetValueAsUnsigned()
		) != 0 else False

		return False

	def has_children(self):
		return True


def LazySummary(valobj, _dict):
	computed = valobj.GetNumChildren() > 0;
	return f"Is Computed={'true' if computed else 'false'}"


def __lldb_init_module(debugger, _dict):
	typeName = r"(^folly::detail::Lazy<.*$)"
	moduleName = os.path.splitext(os.path.basename(__file__))[0]

	debugger.HandleCommand(
		'type synthetic add '
		+ f'-x "{typeName}" '
		+ f'--python-class {moduleName}.LazyFormatter'
	)

	debugger.HandleCommand(
		'type summary add --expand --hide-empty --no-value ' 
		+ f'-x "{typeName}" ' 
		+ f'--python-function {moduleName}.LazySummary'
	)
