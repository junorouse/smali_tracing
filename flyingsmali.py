import argparse
import glob

parser = argparse.ArgumentParser(description='Hack with smali code caving')
parser.add_argument('--tracsm', help='inject tracing smali\n--tracsm [dir]')
parser.add_argument('--fileread', help='generate dynamic changable smali code\n--fileread')

args = parser.parse_args()

def tracing_smali(path):
    glob_iter = glob.glob("{}/*.smali".format(path))

    for g in glob_iter:
        with open(g, 'rb') as f:
            source = f.read()
            f.close()

        source = source.split("\n")

        package = ""
        method = ""
        new_source = ""

        for s in source:
            if s.strip().startswith(".class"):
                package = s.split(";")[0].split(" ")[-1]
                code = s
            elif s.strip().startswith(".method p"): # private, public, protected
                tmp = s.split(".method p")[1].split(" ")[1:]
                method = " ".join(tmp)
                code = s
            elif s.strip().startswith(".locals "):
                tmp = int(s.strip().split(".locals ")[1])
                if tmp < 3:
                    code = ".locals 3"
                else:
                    code = s
                code += "\n"
                code += """
.line 999
const-string v0, "JunoLogCatWWWW"
const-string v1, "{} -> {}"
invoke-static {{v0, v1}},
Landroid/util/Log;->i(Ljava/lang/String;Ljava/lang/String;)I
                """.format(package, method)
            else:
                code = s

            new_source += code + "\n"


        print package
        print method
        print new_source

        with open(g, 'wb') as f:
            f.write(new_source)
            f.close()
     
    return


if args.tracsm is not None:
    tracing_smali(args.tracsm)
else:
    print "Paste this !!!"
    print """
.line 57
new-instance v1, Lcom/example/seccon2015/rock_paper_scissors/Load;

invoke-direct {v1}, Lcom/example/seccon2015/rock_paper_scissors/Load;-><init>()V

.line 58
.local v1, "ab":Lcom/example/seccon2015/rock_paper_scissors/Load;
invoke-static {p0}, Lcom/example/seccon2015/rock_paper_scissors/Load;->LoadFiles(Landroid/app/Activity;)Ljava/lang/String;

move-result-object v5
    """

