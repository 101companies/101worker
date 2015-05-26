#!/usr/bin/env runhaskell

import Text.JSON
import System.Exit
import Language.Haskell.Syntax
import Language.Haskell.Parser
import Data.Maybe
import qualified Data.Text as T


-- Read source code from stdin, write extracted facts to stdout
main = do
   input <- getContents
   let lines = toLines input
   case parseModule input of
     (ParseFailed _ _) -> do
       putStrLn "Haskell parser failed."
       abnormal
     (ParseOk (HsModule _ _ _ imports decls)) -> do
       putStrLn (
        showJSValue (
         jsonModule
          (map extractImport imports)
          (catMaybes (extractFragments lines decls)))
        "")


-- Convert input into newline-separated lines with trimming
toLines :: String -> [String]
toLines = map (T.unpack . T.strip . T.pack) . lines


-- Turn imports and fragments into JSON
jsonModule :: [String] -> [(String, String, (Int, Int))] -> JSValue
jsonModule imports fragments =
  JSObject $
  toJSObject
    [
      ( "imports",
        JSArray (map showJSON imports)
      ),
      ( "fragments",
        JSArray (map jsonFragment fragments)
      )
    ]
  where

    -- Turn classifier and name into JSON
    jsonFragment :: (String, String, (Int, Int)) -> JSValue
    jsonFragment (classifier, name, (from, to)) =
      JSObject (
       toJSObject (
        [
          ("classifier", showJSON classifier),
          ("name", showJSON name),
          ("startLine", showJSON from),
          ("endLine", showJSON to)
        ]))


-- Helper for abnormal exit
abnormal = exitWith $ ExitFailure $ 101


-- Extract name of imported module from import declaration
extractImport :: HsImportDecl -> String
extractImport idecl = let (Module str) = importModule idecl in str


-- Extract fragment from declaration
extractFragments :: [String] -> [HsDecl] -> [Maybe (String, String, (Int, Int))]
extractFragments lines [] = []
extractFragments lines (d:ds) =
  let (ds', m) = extractFragment d in m : extractFragments lines ds'

 where
  extractFragment :: HsDecl -> ([HsDecl], Maybe (String, String, (Int, Int)))
  extractFragment (HsTypeDecl _ (HsIdent n) _ _) = (ds, Just ("type", n, range ds))
  extractFragment (HsDataDecl _ _ (HsIdent n) _ _ _) = (ds, Just ("data", n, range ds))
  extractFragment (HsNewTypeDecl _ _ (HsIdent n) _ _ _) = (ds, Just ("newtype", n, range ds))
  extractFragment (HsFunBind (HsMatch _ (HsIdent n) _ _ _:_)) = (ds, Just ("function", n, range ds))
  extractFragment (HsPatBind _ (HsPVar (HsIdent n)) _ _) = (ds, Just ("pattern", n, range ds))
  extractFragment (HsTypeSig _ [HsIdent n] _) = let (c, ds') = binds "function" n ds in (ds', Just (c, n, range ds'))
  extractFragment _ = (ds, Nothing) -- Some declarations may not be handled

  --
  -- Find binds for a previous type signature
  --
  binds :: String -> String -> [HsDecl] -> (String, [HsDecl])
  binds c n (HsFunBind (HsMatch _ (HsIdent n') _ _ _:_):ds) | n==n' = ("function", ds) 
  binds c n (HsPatBind _ (HsPVar (HsIdent n')) _ _:ds) | n==n' = ("pattern", ds)
  binds c _ ds = (c, ds)

  --
  -- Construct a line range
  -- The complete input is given for examining border of declaration.
  -- All subsequent decls (if any) are given as well.
  --
  range :: [HsDecl] -> (Int, Int)
  range ds =
    case ds of
      (d':_) -> (include (lineNo d), exclude (lineNo d' - 1))
      [] -> (include (lineNo d), length lines)
  --
  -- Include preceding comment
  -- We search upwards for line comments and include them.
  -- We also include white prior to hitting comments and between comment lines.
  -- Whitespace above the comment is not included.
  --
  include :: Int -> Int
  include i = include' i i
    where
      include' i 1 = i
      include' i i' | lines !! (i'-2) == "" = include' i (i'-1)
      include' i i' | take 2 (lines !! (i'-2)) == "--" = include' (i'-1) (i'-1)
      include' i _ = i
  --
  -- Exclude subsequent whitespace/comment
  -- We search upwards for line comments and whitespace and include them.
  -- 
  exclude :: Int -> Int
  exclude i | lines !! (i-1) == "" = exclude (i-1)
  exclude i | take 2 (lines !! (i-1)) == "--" = exclude (i-1)
  exclude i = i

-- Extract source location (line number) from given declaration
lineNo :: HsDecl -> Int
lineNo = srcLine . lineNo'
 where
  lineNo' :: HsDecl -> SrcLoc
  lineNo' (HsTypeDecl x _ _ _) = x
  lineNo' (HsDataDecl x _ _ _ _ _) = x
  lineNo' (HsInfixDecl x _ _ _) = x
  lineNo' (HsNewTypeDecl x _ _ _ _ _) = x
  lineNo' (HsClassDecl x _ _ _ _) = x	 
  lineNo' (HsInstDecl x _ _ _ _) = x	 
  lineNo' (HsDefaultDecl x _) = x	 
  lineNo' (HsTypeSig x _ _) = x
  lineNo' (HsFunBind (HsMatch x _ _ _ _:_)) = x	 
  lineNo' (HsPatBind x _ _ _) = x	 
  lineNo' (HsForeignImport x _ _ _ _ _) = x
  lineNo' (HsForeignExport x _ _ _ _) = x	 
