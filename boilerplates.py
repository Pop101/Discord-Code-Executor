# From https://raw.githubusercontent.com/engineer-man/piston-bot/master/src/cogs/utils/codeswap.py
'''
Copyright (c) 2021 Brian Seymour and EMKC Contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

supported_languages = ('java', 'scala', 'rust', 'c', 'cpp', 'go', 'csharp', 'lolcode')

def add_boilerplate(language, source):
    if language == 'java':
        return for_java(source)
    if language == 'scala':
        return for_scala(source)
    if language == 'rust':
        return for_rust(source)
    if language == 'c' or language == 'cpp':
        return for_c_cpp(source)
    if language == 'go':
        return for_go(source)
    if language == 'csharp':
        return for_csharp(source)
    if language == 'lolcode':
        return for_lolcode(source)
    return source

def for_go(source):
    if 'main' in source:
        return source

    package = ['package main']
    imports = []
    code = ['func main() {']

    lines = source.split('\n')
    for line in lines:
        if line.lstrip().startswith('import'):
            imports.append(line)
        else:
            code.append(line)

    code.append('}')
    return '\n'.join(package + imports + code)

def for_c_cpp(source):
    if 'main' in source:
        return source

    imports = []
    code = ['int main() {']

    lines = source.replace(';', ';\n').split('\n')
    for line in lines:
        if line.lstrip().startswith('#include'):
            imports.append(line)
        else:
            code.append(line)

    code.append('}')
    return '\n'.join(imports + code)

def for_csharp(source):
    if 'static void Main' in source:
        return source

    imports=[]
    code = ['class Program{static void Main(string[] args){']

    lines = source.replace(';', ';\n').split('\n')
    for line in lines:
        if line.lstrip().startswith('using'):
            imports.append(line)
        else:
            code.append(line)
    code.append('}}')
    return '\n'.join(imports + code)

def for_java(source):
    if 'class' in source:
        return source

    imports = []
    code = [
        'public class temp extends Object {public static void main(String[] args) {']

    lines = source.replace(';', ';\n').split('\n')
    for line in lines:
        if line.lstrip().startswith('import'):
            imports.append(line)
        else:
            code.append(line)

    code.append('}}')
    return '\n'.join(imports + code)

def for_scala(source):
    if any(s in source for s in ('extends App', 'def main', '@main def', '@main() def')):
        return source

    # Scala will complain about indentation so just indent source
    indented_source = '  ' + source.replace('\n', '\n  ').rstrip() + '\n'

    return f'@main def run(): Unit = {{\n{indented_source}}}\n'

def for_rust(source):
    if 'fn main' in source:
        return source
    imports = []
    code = ['fn main() {']

    lines = source.replace(';', ';\n').split('\n')
    for line in lines:
        if line.lstrip().startswith('use'):
            imports.append(line)
        else:
            code.append(line)

    code.append('}')
    return '\n'.join(imports + code)

def for_lolcode(source):
    if 'HAI ' in source:
        return source

    code = ['HAI 1.2']

    lines = source.split('\n')
    for line in lines:
            code.append('\t'+line)

    code.append('KTHXBYE')
    return '\n'.join(code)