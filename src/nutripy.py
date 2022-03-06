import pandas as pd
import json

class NutriPy:
    def __init__(self):
        self.columns = {
            'food_name': 'food',
            'category': 'category',
            'serving_size': 'serving_size',
            'fullness_factor': 'fullness_factor',
            'completeness_score': 'completeness_score',
            'calories': 'calories',
            'total_carbs': 'total_carbs',
            'dietary_fibre': 'dietary_fibre',
            'starch': 'starch',
            'sugars': 'sugars',
            'total_fat': 'total_fat',
            'saturated_fat': 'saturated_fat',
            'monosaturated_fat': 'monosaturated_fat',
            'polysaturated_fat': 'polysaturated_fat',
            'protien': 'protien',
            'water': 'water',
            'source': 'source'
        }
        self.df = pd.read_csv('main_csv.csv')

    def getColumnHeaders(self):
        return list(self.columns.keys())

    def getValidOperations(self):
        return ['>', '<', '==', '!=', '>=', '<=']

    def getMathableColumns(self):
        return [key for key in self.columns if (key not in ['food_name', 'category', 'source'])]

    def getOperationResults(self, column: str, op: str, value: float):
        if (op in self.getValidOperations()):
            result = []
            if (op == '=='):
                result = self.df[self.df[self.columns[column]] == value]
            elif (op == '<='):
                result = self.df[self.df[self.columns[column]] <= value]
            elif (op == '>='):
                result = self.df[self.df[self.columns[column]] >= value]
            elif (op == '>'):
                result = self.df[self.df[self.columns[column]] > value]
            elif (op == '<'):
                result = self.df[self.df[self.columns[column]] < value]
            elif (op == '!='):
                result = self.df[self.df[self.columns[column]] != value]
            return result
        else:
            raise ValueError(op + ' operation is invalid, valid operations are ' + str(self.getValidOperations()))

    def getFormattedFood(self, df: pd.DataFrame):
        data = json.loads(df.sort_values(self.columns['food_name']).to_json(orient='records').replace('\/', '/'))
        formattedData = []
        for food in data:
            formattedData.append({})
            for key, value in food.items():
                formattedData[-1][key] = float(value) if ('.' in str(value) and str(value).split('.')[0].isdigit()) else value
        return formattedData

    def getFoodById(self, id: int, asdf: bool = False):
        if (id > 0 and id < len(self.df)):
            result = self.df[id: id + 1]
            return self.getResults(result, asdf)
        raise ValueError('id must be in range [1, ' + len(self.df) + '] and an int value')

    def getFoodsByName(self, name: str, exact: bool = False, asdf: bool = False):
        return self.searchByValue('food_name', name, exact, asdf)

    def getFoodsByCategory(self, category: str, exact: bool = False, asdf: bool = False):
        return self.searchByValue('category', category, exact, asdf)

    def getFoods(self, column: str, cond: str = '', asdf: bool = False):
        # input: column, cond (ex: '> 2', '== 4.21')
        if (column in self.getMathableColumns()):
            result = self.getOperationResults(column, cond.split(' ')[0], float(cond.split(' ')[1]))
            return self.getResults(result, asdf)
        else:
            raise ValueError('cannot perform "' + cond.split(' ')[0] + '" operation on column ' + column)

    def getResults(self, result: pd.DataFrame, asdf: bool):
        return self.getFormattedFood(result) if (not asdf) else result

    def searchByValue(self, column: str, value, exact: bool = False, asdf: bool = False):
        if (type(value) == str):
            result = self.df[self.df[self.columns[column]].str.contains(value.strip(), case=False)] if (not exact) \
                else self.getOperationResults(column, '==', value.strip())
        elif (type(value) in [int, float]):
            result = self.getOperationResults(column, '==', float(value))
        return self.getResults(result, asdf)

    def setColumnHeaders(self, headers: dict):
        if (set(list(headers.keys()).sort()) == set(list(self.columns.keys()).sort())):
            if (any([type(val) != str for val in list(headers.values())])):
                raise ValueError('all values must be strings')
            self.columns.update(headers)
        else:
            raise ValueError('given dict contains values that are not defined, accepted keys are: ' + str(list(self.columns.keys())))

nutri = NutriPy()

#print(nutri.getFoodById(23))
#print(len(nutri.getFoods('polysaturated_fat', '>= 1')))
print(nutri.getFoodsByName('Alcoholic beverage'))
#print(nutri.getFoodsByCategory('breakfast', True))