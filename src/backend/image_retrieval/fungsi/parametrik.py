package functions;

import main.IO;
import matrix.*;

/* Setiap method membuat instansi SPL sebagai nilai yang akan di return. 
   Oleh karena itu, penggunaan di luar Class ini tidak perlu membuat instance baru
   
   Setiap instance memiliki 3 state, oneSolution, infSolution dan noSolution.
   Solusi unik dinyatakan dalam sebuah array solusi.
   Tidak ada solusi cukup dengan state no solution, display "tidak ada solusi" ditulis
   pada Main.
   Solusi dependent (Infinite Solutions) dinyatakan dalam prametrik 
 */

public class SPL {
    boolean oneSolution;
    boolean noSolution;
    boolean infSolution;
    double[] solutions;
    String[] paramSolutions;
    int variables;
    
    // Contructor
    public SPL(int varCount){
        this.oneSolution = false;
        this.noSolution = false;
        this.infSolution = false;
        this.solutions = new double[varCount];
        this.paramSolutions = new String[varCount];
        this.variables = this.solutions.length; 
    }

    public void setOneSolution() {oneSolution = true;}
    public void setNoSolution() {noSolution = true;}
    public void setInfSolution() {infSolution = true;}
    public boolean isOneSolution() {return oneSolution;}
    public boolean isNoSolution() {return noSolution;}
    public boolean isInfSolution() {return infSolution;}
    public void setSolutions(int Idx, double val){solutions[Idx] = val;}
    public void setParamSolutions(int Idx, String val){paramSolutions[Idx] = val;}
    public double getSolutions(int Idx){return solutions[Idx];}
    public String getParamSolutions(int Idx){return paramSolutions[Idx];}
    public int varCount(){return variables;}
    public void displaySolutions(){
        for(int i = 0; i < variables; i++){
            if(oneSolution){System.out.print("X" + (i+1) + " = " + solutions[i] + " ");}
            else if(infSolution){
                System.out.print("X" + (i+1) + " = " + paramSolutions[i] + " ");
                if (paramSolutions[i].isEmpty()){
                    System.out.print("0");
                }
            }
            System.out.println("");
        }
    }


    // Dipakai pada RREF Form
    public static SPL parametricWriter(Matrix M) {
        int row = M.rowCount(), col = M.colCount() - 1;
        int i, j, k;
        boolean[] isFreeVariable = new boolean[col];
        double[] constantsHolder = new double[col];
        String params = "abcdefghijklmnopqrstuvwxyz";
        int paramCount = 0;
        SPL result = new SPL(col);

        // Initialize paramSolutions and isFreeVariable;
        for (i = 0; i < col; i++) {
            result.setParamSolutions(i, "");
            isFreeVariable[i] = true;
        }

         // Find all the free variables
        for(i = 0 ; i < row; i++){
             for( j = 0; j< col; j++){
                if(M.getElmt(i, j) == 1 ){
                    isFreeVariable[j] = false;
                    constantsHolder[j] = M.getElmt(i, col);
                    break;
                }
            }
        }
        for (j = 0; j < col; j++){
            
            if (isFreeVariable[j]) {
                // Initialize the free variable with a parameter like t1, t2, etc.
                result.setParamSolutions(j, "" + params.charAt(paramCount));
                paramCount++; // Increment paramCount here for free variables
            }
         }
         int nonFreeCount = 0;
         for(j = 0; j < col; j++){
            if(!isFreeVariable[j]) nonFreeCount++;
         }
         int[] indexHolder = new int[nonFreeCount];
         int indexHolderIdx = 0;
         for(j = 0; j < col; j++){
            if(!isFreeVariable[j]) {
                indexHolder[indexHolderIdx] = j;
                indexHolderIdx++;}
         }
         // Construct Parametric Form
         indexHolderIdx = 0;
         for (i = 0; i < row && indexHolderIdx < nonFreeCount; i++){
                int nonFreeIdx = indexHolder[indexHolderIdx]; // Get the current non-free variable index
                if (M.getElmt(i, nonFreeIdx) == 1) { // Ensure the current row corresponds to this non-free variable
                    double constant = constantsHolder[nonFreeIdx]; // The constant term for this non-free variable
                    String currSolution = (constant == 0) ? "" : "" + constant;
                
                // For each free variable, print its coefficient with parameter
                for (k = 0; k < col; k++) {
                    if (isFreeVariable[k]) {
                        double coeff = -M.getElmt(i, k);
                        String sign = "+";
                        if (coeff < 0) {
                            coeff = -coeff;
                            sign = "-";
                        }
                        if (coeff != 0){
                            if(!currSolution.isEmpty()) {currSolution += " " + sign + " ";}
                            if (coeff == 1){currSolution += result.paramSolutions[k];}
                            else currSolution += coeff + result.paramSolutions[k];
                        }
                        
                    }
                }
                result.setParamSolutions(nonFreeIdx, currSolution);
                indexHolderIdx++;
                }
        }
        return result;
    }
    public static void main(String[] args) {
        Matrix M = IO.keyboardInputMatrix(4, 6);
        SPL R = gaussElim(M);
        M = MatrixAdv.getRREMatrix(M);
        R.displaySolutions();
    }
} 