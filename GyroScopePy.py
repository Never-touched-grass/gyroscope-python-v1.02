import re
import math_util
from filemanager import FileManager
fm = FileManager()
funcNames = []
funcCodes = []
lines = []
varNames = []
varVals = []
listNames = []
lists = []
cmd = " "
lineCount = 1
listf = False
mathf = False
print("Currently editing file: main.gs")
fm.new_file("main")
while True:
    cmd = input(str(lineCount) + ".")
    lineCount += 1
    if cmd.startswith("gs--"):
        if cmd == "gs--run":
            break
        elif cmd == "gs--clear":
            lines = []
            varNames = []
            varVals = []
            funcNames = []
            funcCodes = []
            lineCount = 1
            print("File cleared.")
            continue
        elif cmd.startswith("gs--newfile"):
            filename = cmd.replace("gs--newfile ", "").strip()
            try:
                fm.new_file(filename)
                current_file = filename
                lines = []
                lineCount = 1
                print(f"File '{filename}' created and being edited.")
            except ValueError as e:
                print(e)
            continue
        elif cmd.startswith("gs--editfile"):
            filename = cmd.replace("gs--editfile ", "").strip()
            if fm.get_file(filename) is None:
                print(f"File '{filename}' does not exist.")
            else:
                current_file = filename
                content = fm.get_file(filename)
                lines = content.split("\n") if content else []
                print(f"Currently editing file: {filename}")
        elif cmd.startswith("gs--savefile"):
            if not current_file:
                print("No file currently being edited.")
            else:
                fm.files[current_file] = "\n".join(lines)
                print(f"File '{current_file}' saved.")
        elif cmd.startswith("gs--listfiles"):
            print(f"Files: {fm.list_files()}")
        elif cmd.startswith("gs--delfile"):
            filename = cmd.replace("gs--delfile ", "").strip()
            if fm.delete_file(filename):
                current_file = None
                print(f"File '{filename}' deleted.")
                lines = []
                lineCount = 1
            print("Unknown command: " + cmd)
    if cmd.startswith("gs--"):
        pass
    else:
        lines.append(cmd)

i = 0
while i < len(lines):
    line = lines[i]

    if line.startswith("print> "):
        st = line.replace("print> ", "")
        if st.startswith('"') and st.endswith('"'):
            out = re.sub('"', '', st)
            print(out, end="")
        else:
            for j in range(len(varNames)):
                if varNames[j] == st:
                    if isinstance(varVals[j], str) and varVals[j].startswith('"') and varVals[j].endswith('"'):
                        print(varVals[j].replace('"', '').strip())
                    elif isinstance(varVals[j], ()):
                        print(int(varVals[j]), end="")
                    else:
                       for x in range(len(varNames)):
                           if varNames[x] == varVals[j]:
                               print(varVals[x], end="")
        i += 1
    elif line.startswith("println> "):
        st = line.replace("println> ", "")
        if st.startswith('"') and st.endswith('"'):
            out = re.sub('"', '', st)
            print(out)
        else:
            for j in range(len(varNames)):
                if varNames[j] == st:
                    if isinstance(varVals[j], str) and varVals[j].startswith('"') and varVals[j].endswith('"'):
                        print(varVals[j].replace('"', '').strip())
                    elif isinstance(varVals[j], (int, float)):
                        print(int(varVals[j]))
                    else:
                       for x in range(len(varNames)):
                           if varNames[x] == varVals[j]:
                               print(varVals[x])
        i += 1
    elif line.startswith("var> "):
        st = line.replace("var> ", '')
        prs = st.split(' ')
        if len(prs) >= 3:
            if prs[2] == "e>":
                varNames.append(prs[0])
                varVals.append(eval(" ".join(prs[3:]).strip()))
            else:
                varNames.append(prs[0])
                varVals.append(" ".join(prs[2:]).strip())
        i += 1

    elif line.startswith("if> "):
        cond = line.replace("if> ", '').strip()
        tokens = cond.split(' ')

        skip = False
        try:
            left = tokens[0]
            op = tokens[1]
            right = tokens[2]

            for idx, name in enumerate(varNames):
                if varNames[idx] == left:
                    left = varVals[idx]
                if varNames[idx] == right:
                    right = varVals[idx]

            try:
                left = int(left)
            except:
                pass
            try:
                right = int(right)
            except:
                pass

            expression = f"{repr(left)} {op} {repr(right)}"
            if not eval(expression):
                skip = True

        except Exception as e:
            print(f"Invalid if condition: {cond} -> {e}")
            skip = True

        if skip:
            while i < len(lines) and lines[i] != "}":
                i += 1
        i += 1

    elif line.startswith("while> "):
        cond = line.replace("while> ", '').split(' ')
        loop_var = cond[0]
        loop_op = cond[1]
        loop_val = cond[2]

        loop_body = []
        j = i + 1
        while j < len(lines) and lines[j] != "}":
            loop_body.append(lines[j])
            j += 1

        var_index = -1
        for x in range(len(varNames)):
            if varNames[x] == loop_var:
                var_index = x
                break

        if var_index == -1:
            print(f"Variable {loop_var} not found.")
            i = j + 1
            continue

        while eval(f"{int(varVals[var_index])} {loop_op} {loop_val}"):
            for body_line in loop_body:
                if body_line.startswith("print> "):
                    st = body_line.replace("print> ", "")
                    if st.startswith('"') and st.endswith('"'):
                        out = re.sub('"', '', st)
                        print(out, end="")
                    else:
                        for j in range(len(varNames)):
                            if varNames[j] == st:
                                print(varVals[j], end="")

                elif body_line.startswith("println> "):
                    st = body_line.replace("println> ", "")
                    if st.startswith('"') and st.endswith('"'):
                        out = re.sub('"', '', st)
                        print(out)
                    else:
                        for j in range(len(varNames)):
                            if varNames[j] == st:
                                print(varVals[j])

                elif body_line.endswith("++"):
                    varname = body_line.replace("++", "").strip()
                    for j in range(len(varNames)):
                        if varNames[j] == varname:
                            varVals[j] = str(int(varVals[j]) + 1)

                elif body_line.startswith("var> "):
                    st = body_line.replace("var> ", '')
                    prs = st.split(' ')
                    if len(prs) >= 3:
                        if prs[2] == "e>":
                            varNames.append(prs[0])
                            varVals.append(eval(" ".join(prs[3:]).strip()))
                        elif prs[2].startswith("math.fib>"):
                            if not mathf:
                                print("ERROR: 'math' not defined. Did you forget to require> mathf?")
                                continue
                            num = prs[2].replace("math.fib>", "").strip()
                            try:
                                num = int(num)
                                varNames.append(prs[0])
                                varVals.append(math_util.fib(num))
                            except ValueError:
                                print(f"Invalid number for fib: {num}")
                        else:
                            varNames.append(prs[0])
                            varVals.append(" ".join(prs[2:]).strip())

                elif body_line.startswith("read> "):
                    v = body_line.replace("read> ", '').strip()
                    for n in range(len(varNames)):
                        if varNames[n] == v:
                            varVals[n] = input("")
                            break

                elif body_line.startswith("if> "):
                    cond = body_line.replace("if> ", '').strip().split(' ')
                    try:
                        left = cond[0]
                        op = cond[1]
                        right = cond[2]

                        for idx, name in enumerate(varNames):
                            if varNames[idx] == left:
                                left = varVals[idx]
                            if varNames[idx] == right:
                                right = varVals[idx]

                        try:
                            left = int(left)
                        except:
                            pass
                        try:
                            right = int(right)
                        except:
                            pass

                        if not eval(f"{repr(left)} {op} {repr(right)}"):
                            skip_idx = loop_body.index(body_line) + 1
                            while skip_idx < len(loop_body) and loop_body[skip_idx] != "}":
                                skip_idx += 1
                            continue
                    except Exception as e:
                        print(f"Invalid if in while loop: {cond} -> {e}")

                elif body_line.startswith("list>"):
                    if not listf:
                        print("ERROR: 'list>' not defined. Did you forget to require> listf?")
                        continue
                    prs = body_line.split(' ', 2)
                    if len(prs) < 3:
                        print("Invalid list declaration.")
                        continue
                    lname = prs[1]
                    lcontent = prs[2].strip()
                    if lcontent.startswith("[") and lcontent.endswith("]"):
                        lcontent = lcontent[1:-1].strip()
                    elif lcontent.startswith("math.fib>"):
                        if not mathf:
                            print("ERROR: 'math' not defined. Did you forget to require> mathf?")
                            i+= 1
                            continue
                        try:
                            num = int(lcontent.replace("math.fib>", "").strip())
                            lcontent = ", ".join(str(math_util.fib(i)) for i in range(num))
                        except ValueError:
                            print(f"Invalid value for fib: {lcontent}")
                            i+= 1
                            continue
                    else:
                        print("Invalid list syntax. Use list> name [item1, item2, ...]")
                        continue
                    elems = []
                    for el in lcontent.split(', '):
                        el = el.strip()
                        if el.startswith('"') and el.endswith('"'):
                            el = el[1:-1]
                        elif el.isdigit():
                            el = int(el)
                        elems.append(el)
                    listNames.append(lname)
                    lists.append(elems)

                elif body_line.startswith("printl> "):
                    for l in range(len(listNames)):
                        if listNames[l] == body_line.replace("printl> ", '').strip():
                            print(lists[l])
                            break

                elif body_line.startswith("require> "):
                    modulename = body_line.replace("require> ", '').strip()
                    if modulename == "listf":
                        listf = True

        i = j + 1

    elif line.startswith("func> "):
        prs = line.replace("func> ", '').split(' ')
        funcNames.append(prs[0])
        funcCodes.append([])
        i += 1
        while i < len(lines) and lines[i] != "}":
            funcCodes[-1].append(lines[i])
            i += 1
        i += 1

    elif line.endswith("()"):
        funcName = line.replace("()", '').strip()
        for f in range(len(funcNames)):
            if funcNames[f] == funcName:
                for k in reversed(range(len(funcCodes[f]))):
                    lines.insert(i + 1, funcCodes[f][k])
        i += 1

    elif line.startswith("read> "):
        v = line.replace("read> ", '').strip()
        for n in range(len(varNames)):
            if varNames[n] == v:
                varVals[n] = input("")
                break
        i+= 1
    elif line.startswith("list>"):
        if not listf:
            print("ERROR: 'list>' not defined. Did you forget to require> listf?")
            i += 1
            continue
        prs = line.split(' ', 2)
        if len(prs) < 3:
            print("Invalid list declaration.")
            i += 1
            continue
        lname = prs[1]
        lcontent = prs[2].strip()

        elems = []
        if lcontent.startswith("[") and lcontent.endswith("]"):
            lcontent = lcontent[1:-1].strip()
            for el in lcontent.split(', '):
                el = el.strip()
                if el.startswith('"') and el.endswith('"'):
                    el = el[1:-1]
                elif el.isdigit():
                    el = int(el)
                elems.append(el)
        elif lcontent.startswith("math.fib>"):
            if not mathf:
                print("ERROR: 'math' not defined. Did you forget to require> mathf?")
                i += 1
                continue
            try:
                num = int(lcontent.replace("math.fib>", "").strip())
                elems = [math_util.fib(n) for n in range(num)][-1]
            except ValueError:
                print(f"Invalid value for fib: {lcontent}")
                i += 1
                continue
        else:
            print("Invalid list syntax. Use list> name [item1, item2, ...] or math.fib>")
            i += 1
            continue

        listNames.append(lname)
        lists.append(elems)
        i += 1
    elif line.startswith("require> "):
        modulename = line.replace("require> ", '').strip()
        if modulename == "listf":
            listf = True
        elif modulename == "mathf":
            mathf = True
        i+= 1
    elif line.startswith("printl> "):
        for l in range(len(listNames)):
            if listNames[l] == line.replace("printl> ", '').strip():
                print(lists[l])
                break
        i+= 1
    elif line.endswith("++"):
        for x in range(len(varNames)):
            if varNames[x] == line.replace("++", '').strip():
                if isinstance(varVals[x], int):
                    varVals[x] += 1
                elif isinstance(varVals[x], float):
                    varVals[x] += 1.0
                else:
                    print("ERROR: Cannot increment non-numeric variable.")
    else:
        if not line == "}":
            print("ERROR: " + line + " is not defined.")
        i += 1 
