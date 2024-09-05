// Add this to google sheets to allow export of sheet to JSON
// Includes functions for exporting active sheet or all sheets as JSON object (also Python object syntax compatible).
// Tweak the makePrettyJSON_ function to customize what kind of JSON to export.


let FORMAT_ONELINE = 'One-line';
let FORMAT_MULTILINE = 'Multi-line';
let FORMAT_PRETTY = 'Pretty';

let LANGUAGE_JS = 'JavaScript';
let LANGUAGE_PYTHON = 'Python';

let STRUCTURE_LIST = 'List';
let STRUCTURE_HASH = 'Hash (keyed by "id" column)';

/* Defaults for this particular spreadsheet, change as desired */
let DEFAULT_FORMAT = FORMAT_PRETTY;
let DEFAULT_LANGUAGE = LANGUAGE_JS;
let DEFAULT_STRUCTURE = STRUCTURE_LIST;

/* This will add a child JSON Obj at the end of the row */
const CHILD_JSON_NAME = "ratings";
const CHILD_JSON_VALUES = ["ALT_CORE_B_AX_01_C", "ALT_CORE_B_AX_02_C", "ALT_CORE_B_AX_03_C"]


function onOpen() {
    let ss = SpreadsheetApp.getActiveSpreadsheet();
    let menuEntries = [
        {name: "Export JSON for this sheet", functionName: "exportSheet"},
        {name: "Export JSON for all sheets", functionName: "exportAllSheets"}
    ];
    ss.addMenu("Export JSON", menuEntries);
}

function makeLabel(app, text, id) {
    let lb = app.createLabel(text);
    if (id) lb.setId(id);
    return lb;
}

function makeListBox(app, name, items) {
    let listBox = app.createListBox().setId(name).setName(name);
    listBox.setVisibleItemCount(1);

    let cache = CacheService.getPublicCache();
    let selectedValue = cache.get(name);
    Logger.log(selectedValue);
    for (let i = 0; i < items.length; i++) {
        listBox.addItem(items[i]);
        if (items[1] == selectedValue) {
            listBox.setSelectedIndex(i);
        }
    }
    return listBox;
}

function makeButton(app, parent, name, callback) {
    let button = app.createButton(name);
    app.add(button);
    let handler = app.createServerClickHandler(callback).addCallbackElement(parent);
    ;
    button.addClickHandler(handler);
    return button;
}

function makeTextBox(app, name) {
    let textArea = app.createTextArea().setWidth('100%').setHeight('200px').setId(name).setName(name);
    return textArea;
}

function exportAllSheets(e) {

    let ss = SpreadsheetApp.getActiveSpreadsheet();
    let sheets = ss.getSheets();
    let sheetsData = {};
    for (let i = 0; i < sheets.length; i++) {
        let sheet = sheets[i];
        let rowsData = getRowsData_(sheet, getExportOptions(e));
        let sheetName = sheet.getName();
        sheetsData[sheetName] = rowsData;
    }
    let json = makeJSON_(sheetsData, getExportOptions(e));
    displayText_(json);
}

function exportSheet(e) {
    let ss = SpreadsheetApp.getActiveSpreadsheet();
    let sheet = ss.getActiveSheet();
    let rowsData = getRowsData_(sheet, getExportOptions(e));
    let json = makeJSON_(rowsData, getExportOptions(e));
    displayText_(json);
}

function getExportOptions(e) {
    let options = {};

    options.language = e && e.parameter.language || DEFAULT_LANGUAGE;
    options.format = e && e.parameter.format || DEFAULT_FORMAT;
    options.structure = e && e.parameter.structure || DEFAULT_STRUCTURE;

    let cache = CacheService.getPublicCache();
    cache.put('language', options.language);
    cache.put('format', options.format);
    cache.put('structure', options.structure);

    Logger.log(options);
    return options;
}

function makeJSON_(object, options) {
    let jsonString = JSON.stringify(object, null, 4);
    if (options.format === FORMAT_PRETTY) {
        // use default
    } else if (options.format === FORMAT_MULTILINE) {
        jsonString = Utilities.jsonStringify(object);
        jsonString = jsonString.replace(/},/gi, '},\n');
        jsonString = prettyJSON.replace(/":\[{"/gi, '":\n[{"');
        jsonString = prettyJSON.replace(/}\],/gi, '}],\n');
    } else {
        jsonString = Utilities.jsonStringify(object);
    }
    if (options.language === LANGUAGE_PYTHON) {
        // add unicode markers
        jsonString = jsonString.replace(/"([a-zA-Z]*)":\s+"/gi, '"$1": u"');
    }
    return jsonString;
}

function displayText_(text) {
    let output = HtmlService.createHtmlOutput("<textarea style='width:100%;' rows='20'>" + text + "</textarea>");
    output.setWidth(400)
    output.setHeight(300);
    SpreadsheetApp.getUi()
        .showModalDialog(output, 'Exported JSON');
}

// getRowsData iterates row by row in the input range and returns an array of objects.
// Each object contains all the data for a given row, indexed by its normalized column name.
function getRowsData_(sheet) {
    let headersRange = sheet.getRange(1, 1, sheet.getFrozenRows(), sheet.getMaxColumns());
    let headers = headersRange.getValues()[0];
    let dataRange = sheet.getRange(sheet.getFrozenRows() + 1, 1, sheet.getMaxRows(), sheet.getMaxColumns());
    let objects = getObjects_(dataRange.getValues(), normalizeHeaders_(headers));
    return objects;

}

// getColumnsData iterates column by column in the input range and returns an array of objects.
// Each object contains all the data for a given column, indexed by its normalized row name.
// Arguments:
//   - sheet: the sheet object that contains the data to be processed
//   - range: the exact range of cells where the data is stored
//   - rowHeadersColumnIndex: specifies the column number where the row names are stored.
//       This argument is optional and it defaults to the column immediately left of the range;
// Returns an Array of objects.
function getColumnsData_(sheet, range, rowHeadersColumnIndex) {
    rowHeadersColumnIndex = rowHeadersColumnIndex || range.getColumnIndex() - 1;
    let headersTmp = sheet.getRange(range.getRow(), rowHeadersColumnIndex, range.getNumRows(), 1).getValues();
    let headers = normalizeHeaders_(arrayTranspose_(headersTmp)[0]);
    return getObjects(arrayTranspose_(range.getValues()), headers);
}


// For every row of data in data, generates an object that contains the data. Names of
// object fields are defined in keys.
// Arguments:
//   - data: JavaScript 2d array
//   - keys: Array of Strings that define the property names for the objects to create
function getObjects_(data, keys) {
    let objects = [];

    for (let i = 0; i < data.length; ++i) {
        let object = {};
        let hasData = false;
        for (let j = 0; j < data[i].length; ++j) {
            let cellData = data[i][j];
            if (isCellEmpty_(cellData)) {
                continue;
            }
            object[keys[j]] = cellData;
            hasData = true;
        }

        if (hasData) {
            if (CHILD_JSON_NAME !== "") {
                object[CHILD_JSON_NAME] = {};
                CHILD_JSON_VALUES.forEach((element) => {
                        if (element in object) {
                            object[CHILD_JSON_NAME][element] = object[element];
                        }
                    }
                );
            }
            objects.push(object);
        }
    }
    return objects;
}

// Returns an Array of normalized Strings.
// Arguments:
//   - headers: Array of Strings to normalize
function normalizeHeaders_(headers) {
    let keys = [];
    for (let i = 0; i < headers.length; ++i) {
        let key = headers[i];
        if (key.length > 0) {
            keys.push(key);
        }
    }
    return keys;
}

// Normalizes a string, by removing all alphanumeric characters and using mixed case
// to separate words. The output will always start with a lower case letter.
// This function is designed to produce JavaScript object property names.
// Arguments:
//   - header: string to normalize
// Examples:
//   "First Name" -> "firstName"
//   "Market Cap (millions) -> "marketCapMillions
//   "1 number at the beginning is ignored" -> "numberAtTheBeginningIsIgnored"
function normalizeHeader_(header) {
    let key = "";
    let upperCase = false;
    for (let i = 0; i < header.length; ++i) {
        let letter = header[i];
        if (letter === " " && key.length > 0) {
            upperCase = true;
            continue;
        }
        if (!isAlnum_(letter)) {
            continue;
        }
        if (key.length === 0 && isDigit_(letter)) {
            continue; // first character must be a letter
        }
        if (upperCase) {
            upperCase = false;
            key += letter.toUpperCase();
        } else {
            key += letter.toLowerCase();
        }
    }
    return key;
}

// Returns true if the cell where cellData was read from is empty.
// Arguments:
//   - cellData: string
function isCellEmpty_(cellData) {
    return typeof (cellData) == "string" && cellData == "";
}

// Returns true if the character char is alphabetical, false otherwise.
function isAlnum_(char) {
    return char >= 'A' && char <= 'Z' ||
        char >= 'a' && char <= 'z' ||
        isDigit_(char);
}

// Returns true if the character char is a digit, false otherwise.
function isDigit_(char) {
    return char >= '0' && char <= '9';
}

// Given a JavaScript 2d Array, this function returns the transposed table.
// Arguments:
//   - data: JavaScript 2d Array
// Returns a JavaScript 2d Array
// Example: arrayTranspose([[1,2,3],[4,5,6]]) returns [[1,4],[2,5],[3,6]].
function arrayTranspose_(data) {
    if (data.length === 0 || data[0].length === 0) {
        return null;
    }

    let ret = [];
    for (let i = 0; i < data[0].length; ++i) {
        ret.push([]);
    }

    for (let i = 0; i < data.length; ++i) {
        for (let j = 0; j < data[i].length; ++j) {
            ret[j][i] = data[i][j];
        }
    }

    return ret;
}