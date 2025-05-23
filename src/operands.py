from utils import Utils
import pandas as pd

class Operands():
	def __init__(self, fleft, fright, cleft, cright, output):
		self.output = output

		self.dfleft = self.read(fleft)
		self.dfright = self.read(fright)

		self.col_name_left = cleft
		self.col_name_right = cright

		if self.dfleft is not None and self.dfright is not None:
			self.col_left = self.dfleft[cleft].to_numpy()
			self.col_right = self.dfright[cright].to_numpy()
		else:
			pass # TODO

		self.initialize_workbook()

	def initialize_workbook(self):
		with pd.ExcelWriter(
			self.output,
			engine='openpyxl',
			mode='w'
		) as writer:
			self.dfleft.to_excel(
		        writer,
		        sheet_name='left',
		        index=False
		    )
			self.dfright.to_excel(
		        writer,
		        sheet_name='right',
		        index=False
		    )

	@staticmethod
	def read(file):
		df = None
		is_valid, ext = Utils.is_valid_file(file)
		if is_valid:
			match ext:
				case '.csv':
					df = pd.read_csv(file)
				case '.xlsx':
					df = pd.read_excel(file)
				case _:
					pass # TODO

		return df

	@staticmethod
	def write(df, sheet_name, output):
		with pd.ExcelWriter(
			output,
			engine='openpyxl',
			mode='a'
		) as writer:
			df.to_excel(
	            writer,
	            sheet_name=sheet_name,
	            index=False
	        )
		

	def left_not_right(self):
		lnr = self.dfleft.loc[
				~self.dfleft[self.col_name_left].isin(self.col_right)
			]

		Operands.write(lnr, 'left_not_right', self.output)
		
	def right_not_left(self):
		rnl = self.dfright.loc[
				~self.dfright[self.col_name_right].isin(self.col_left)
			]

		Operands.write(rnl, 'right_not_left', self.output)

	def intersection(self):
		dfright = self.dfright.rename(columns={self.col_name_right: self.col_name_left})
		
		intersec = pd.merge(
		                    self.dfleft,
		                    dfright,
		                    how='inner',
		                    on=self.col_name_left,
		                    suffixes=('_left', '_right')
		                )

		Operands.write(intersec, 'intersection', self.output)

	def union(self):
		dfright = self.dfright.rename(columns={self.col_name_right: self.col_name_left})
		
		union = pd.concat([
		                  	self.dfleft,
		                  	dfright
		                  ],
		                  ignore_index=True,
		                  names=list(self.dfleft.columns),
		                  join='inner' # Keep only overlapping columns
		                )
		
		union_distinct = union.drop_duplicates()
		
		Operands.write(union_distinct, 'union_distinct', self.output)

	def cartesian(self):
		cartesian = pd.merge(
		                    self.dfleft,
		                    self.dfright,
		                    how='cross',
		                    suffixes=('_left', '_right')
		                )

		Operands.write(cartesian, 'cartesian_product', self.output)
