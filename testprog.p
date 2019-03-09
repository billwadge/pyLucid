[[vpop0 savespace 0 setspace " s eval restorespace] " output ludef 
[savevar setvar waresearch [restorevar] breakc [s] saveplace popplace select eval restoreplace waresave restorevar] " x ludef 
[savevar setvar waresearch [restorevar] breakc [x] saveplace popplace select eval restoreplace waresave restorevar] " y ludef 
[savevar setvar waresearch [restorevar] breakc [V16] saveplace popplace select eval restoreplace waresave restorevar] " q ludef 
[savevar setvar waresearch [restorevar] breakc " I eval savespace setspace " y eval restorespace waresave restorevar] " swvr ludef
 [savevar setvar waresearch [restorevar] breakc [" K eval] [decspace " V12 eval incspace] space 0 eq if waresave restorevar] " I ludef 
 [savevar setvar waresearch [restorevar] breakc [" V08 eval] [" V09 eval] " q eval if waresave restorevar] " K ludef 
 [savevar setvar waresearch [restorevar] breakc " V07 eval pushplace " swvr eval popplace vpop0 waresave restorevar] " er ludef 
 [savevar setvar waresearch [restorevar] breakc [" n2 eval] [dectime " V06 eval inctime] time 0 eq if waresave restorevar] " s ludef 
 [savevar setvar waresearch [restorevar] breakc [" V03 eval] [decspace " V04 eval incspace] space 0 eq if waresave restorevar] " p ludef 
 [savevar setvar waresearch [restorevar] breakc [" V00 eval] [decspace " V02 eval incspace] space 0 eq if waresave restorevar] " n2 ludef 
 [vpop0 " n2 eval " V01 eval +] " V02 ludef [vpop0 " 1] " V01 ludef [vpop0 " 2] " V00 ludef [vpop0 " p eval not] " V04 ludef 
 [vpop0 true] " V03 ludef [savevar setvar waresearch [restorevar] breakc " V05 eval pushplace " er eval popplace vpop0 waresave restorevar] " V06 ludef
  [vpop0 " 0] " V05 ludef [vpop0 " 0] " V07 ludef [vpop0 incspace " K eval decspace] " V09 ludef [vpop0 space] " V08 ludef
   [savevar setvar waresearch [restorevar] breakc " V11 eval savespace setspace " K eval restorespace waresave restorevar] " V12 ludef 
   [vpop0 " I eval " V10 eval +] " V11 ludef [vpop0 " 1] " V10 ludef [vpop0 " V14 eval " V15 eval ne] " V16 ludef [vpop0 " 0] " V15 ludef 
   [vpop0 " x eval " V13 eval mod] " V14 ludef [vpop0 savespace 0 setspace " x eval restorespace] " V13 ludef 
   [" output eval writeln inctime] 10 repeat]
