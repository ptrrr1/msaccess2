from utils import Utils
import pandas as pd
import os

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

	def left_not_right(self):
		lnr = self.dfleft.loc[
				~self.dfleft[self.col_name_left].isin(self.col_right)
			]

		with pd.ExcelWriter(
			self.output,
			engine='openpyxl',
			mode='a'
		) as writer:
			lnr.to_excel(
	            writer,
	            sheet_name="left_not_right",
	            index=False
	        )

	def right_not_left(self):
		rnl = self.dfright.loc[
				~self.dfright[self.col_name_right].isin(self.col_left)
			]

		with pd.ExcelWriter(
			self.output,
			engine='openpyxl',
			mode='a'
		) as writer:
			rnl.to_excel(
		        writer,
		        sheet_name="right_not_left",
		        index=False
		    )

	def intersection(self):
		intersec = pd.merge(
	                    self.dfleft,
	                    self.dfright,
	                    how='inner',
	                    left_on=self.col_name_left,
	                    right_on=self.col_name_right,
	                    suffixes=('_left', '_right')
	                )

		with pd.ExcelWriter(
			self.output,
			engine='openpyxl',
			mode='a'
		) as writer:
			intersec.to_excel(
	            writer,
	            sheet_name='intersection',
	            index=False
	        )

	def union(self):
		pass
